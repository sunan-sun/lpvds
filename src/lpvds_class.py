import os, sys, json
import numpy as np

""" uncomment the imports below if using DAMM; otherwise import your own methods """
from .damm.damm_class import damm_class
from .dsopt.dsopt_class import dsopt_class



def write_json(data, path):
    with open(path, "w") as json_file:
        json.dump(data, json_file, indent=4)




class lpvds_class():
    def __init__(self, x, x_dot, x_att) -> None:
        self.x      = x
        self.x_dot  = x_dot
        self.x_att  = x_att
        self.dim    = 2*x.shape[1]  # either 4 or 6

        # simulation parameters
        self.tol = 10E-3
        self.max_iter = 10000

        # define output path
        file_path           = os.path.dirname(os.path.realpath(__file__))  
        self.output_path    = os.path.join(os.path.dirname(file_path), 'output_pos.json')


    def _cluster(self):
        param ={
            "mu_0":           np.zeros((self.dim, )), 
            "sigma_0":        1 * np.eye(self.dim),
            "nu_0":           self.dim,
            "kappa_0":        1,
            "sigma_dir_0":    1,
            "min_thold":      10
        }

        self.damm  = damm_class(self.x, self.x_dot, param)
        self.gamma = self.damm.begin()

        self.assignment_arr = np.argmax(self.gamma, axis=0)
        self.K     = self.gamma.shape[0]


    def _optimize(self):

        self.ds_opt = dsopt_class(self.x, self.x_dot, self.x_att, self.gamma)
        self.A = self.ds_opt.begin()


    def begin(self):
        self._cluster()
        self._optimize()


    def _step(self, x, dt):
        x_dot     = np.zeros((x.shape[1], 1))

        gamma = self.damm.logProb(x) 
        for k in range(self.K):
            x_dot  += gamma[k, 0] * self.A[k] @ (x - self.x_att).T
        x_next = x + x_dot.T * dt

        return x_next, gamma, x_dot


    def sim(self, x_init, dt):
        x_test = [x_init]
        gamma_test = []
        v_test = []

        i = 0
        while np.linalg.norm(x_test[-1]-self.x_att) >= self.tol:
            if i > self.max_iter:
                print("Exceed max iteration")
                break

            x_next, gamma, v = self._step(x_test[-1], dt)
            x_test.append(x_next)        
            gamma_test.append(gamma[:, 0])
            v_test.append(v)

            i += 1

        return np.vstack(x_test)




    def _logOut(self, *args): 
            Prior = self.damm.Prior
            Mu    = self.damm.Mu
            Sigma = self.damm.Sigma

            json_output = {
                "name": "DAMM-LPVDS",

                "K": self.K,
                "M": Mu.shape[1],
                "Prior": Prior,
                "Mu": Mu.ravel().tolist(),
                "Sigma": Sigma.ravel().tolist(),

                'A': self.A.ravel().tolist(),
                'attractor': self.x_att.ravel().tolist(),
                'att_all': self.x_att.ravel().tolist(),
                "gripper_open": 0
            }

            if len(args) == 0:
                write_json(json_output, self.output_path)
            else:
                write_json(json_output, os.path.join(args[0], '0.json'))
