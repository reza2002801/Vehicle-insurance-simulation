import numpy as np
import matplotlib.pyplot as plt
class WarmUP:
    def __init__(self, num):
        self.warmup_Phq = [[] for i in range(num)]
        self.warmup_Oq = [[] for i in range(num)]
        self.warmup_fq = [[] for i in range(num)]
        self.warmup_eq = [[] for i in range(num)]
        self.warmup_cq = [[] for i in range(num)]
        self.warmup_scq = [[] for i in range(num)]

        self.previous_Phq = 0
        self.previous_Oq = 0
        self.previous_fq = 0
        self.previous_cq = 0
        self.previous_scq = 0
        self.previous_eq = 0


    def res_2_numpy(self):
        self.warmup_Phq1 = np.array(self.warmup_Phq)
        self.warmup_Oq1 = np.array(self.warmup_Oq)
        self.warmup_fq1 = np.array(self.warmup_fq)
        self.warmup_eq1 = np.array(self.warmup_eq)
        self.warmup_cq1 = np.array(self.warmup_cq)
        self.warmup_scq1 = np.array(self.warmup_scq)

    def cal_mean(self):
        self.mean_Phq = np.mean(self.warmup_Phq1, axis=0)
        self.mean_Oq = np.mean(self.warmup_Oq1, axis=0)
        self.mean_fq = np.mean(self.warmup_fq1, axis=0)
        self.mean_eq = np.mean(self.warmup_eq1, axis=0)
        self.mean_cq = np.mean(self.warmup_cq1, axis=0)
        self.mean_scq = np.mean(self.warmup_scq1, axis=0)

    def draw_chart(self):
        x = np.arange(0, self.warmup_Phq1.shape[1])
        for i in range(self.warmup_Phq1.shape[0]):
            plt.plot(x, self.warmup_Phq1[i,:], label='Phq' + str(i))

        smoothed = np.convolve(self.mean_Phq, np.ones(3) / 3, mode='same')
        plt.plot(x, smoothed, label='mean Phq',linewidth=3.0, color='red')
        plt.title('phq')
        plt.show()

        for i in range(self.warmup_Oq1.shape[0]):
            plt.plot(x, self.warmup_Oq1[i,:], label='Oq' + str(i))

        smoothed = np.convolve(self.mean_Oq, np.ones(3) / 3, mode='same')
        plt.plot(x, smoothed, label='mean Oq',linewidth=3.0,color='red')
        plt.title('Oq')
        plt.show()

        for i in range(self.warmup_fq1.shape[0]):
            plt.plot(x, self.warmup_fq1[i,:], label='fq' + str(i))
        smoothed = np.convolve(self.mean_fq, np.ones(3) / 3, mode='same')
        plt.plot(x, smoothed, label='mean fq',linewidth=3.0,color='red')
        plt.title('fq')
        plt.show()

        for i in range(self.warmup_eq1.shape[0]):
            plt.plot(x, self.warmup_eq1[i,:], label='eq' + str(i))
        smoothed = np.convolve(self.mean_eq, np.ones(3) / 3, mode='same')
        plt.plot(x, smoothed, label='mean eq',linewidth=3,color='red')
        plt.title('eq')
        plt.show()

        for i in range(self.warmup_cq1.shape[0]):
            plt.plot(x, self.warmup_cq1[i,:], label='cq' + str(i))
        smoothed = np.convolve(self.mean_cq, np.ones(3) / 3, mode='same')
        plt.plot(x, smoothed, label='mean cq',linewidth=3.0,color='red')
        plt.title('cq')
        plt.show()

        for i in range(self.warmup_scq1.shape[0]):
            plt.plot(x, self.warmup_scq1[i,:], label='scq' + str(i))
        smoothed = np.convolve(self.mean_scq, np.ones(3) / 3, mode='same')
        plt.plot(x, smoothed, label='mean scq',linewidth=3.0 ,color='red')
        plt.title('scq')
        plt.show()


    def clear_vars(self):
        self.previous_cq = 0
        self.previous_scq = 0
        self.previous_eq = 0
        self.previous_fq = 0
        self.previous_Phq = 0
        self.previous_Oq = 0
