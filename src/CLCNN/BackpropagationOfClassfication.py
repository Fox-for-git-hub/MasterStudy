import numpy as np
import matplotlib.pyplot as plt

#座標
X = [np.arange(-1.0, 1.1, 0.1)]
Y = [np.arange(-1.0, 1.1, 0.1)]

##入力と正解の用意##
#入力
input_data = []
#正解
correct_data = []
for x in X:
    for y in Y:
        input_data.append([x, y])
        #y座標系がsinカーブよりも下であれば
        if y < np.sin(np.pi * x):
            #下の領域
            correct_data.append([0, 1])
        else:
            #上の領域
            correct_data.append([1, 0])

#データ数
n_data = len(correct_data)

input_data = np.array(input_data)
correct_data = np.array(correct_data)


##各設定値##
#入力層のニューロン数
n_in = 1
#中間層のニューロン数
n_mid = 6
#出力層のニューロン数
n_out = 1

#重みとバイアスの広がり具合
wb_width = 0.01
#学習係数
eta = 0.1
epoch = 101
#経過の表示間隔
interval = 10


##中間層##
class MiddleLayer:
    #初期設定
    def __init__(self, n_upper, n):
        #重み(行列)とバイアス(ベクトル)
        self.w = wb_width * np.random.randn(n_upper, n)
        self.b = wb_width * np.random.randn(n)

    #順伝播
    def forward(self, x):
        self.x = x
        u = np.dot(x, self.w) + self.b
        #シグモイド関数
        self.y = 1/(1+np.exp(-u))

    #逆伝播
    def backward(self, grad_y):
        #シグモイド関数の微分
        delta = grad_y * (1-self.y)*self.y
        self.grad_w = np.dot(self.x.T, delta)
        self.grad_b = np.sum(delta, axis=0)
        self.grad_x = np.dot(delta, self.w.T)

    # 重みとバイアスの更新
    def update(self, eta):
        self.w -= eta * self.grad_w
        self.b -= eta * self.grad_b


##出力層##

class OutputLayer:
    # 初期設定
    def __init__(self, n_upper, n):
        #重み(行列)
        self.w = wb_width * np.random.randn(n_upper, n)
         #バイアス(ベクトル)
        self.b = wb_width * np.random.randn(n)

    #順伝播
    def forward(self, x):
        self.x = x
        u = np.dot(x, self.w) + self.b
        #恒等関数
        self.y = np.exp(u)/np.sum(np.exp(u), axis=1, keepdims=True)

    #逆伝播
    def backward(self, t):
        delta = self.y - t
        self.grad_w = np.dot(self.x.T, delta)
        self.grad_b = np.sum(delta, axis=0)
        self.grad_x = np.dot(delta, self.w.T)

    # 重みとバイアスの更新
    def update(self, eta):
        self.w -= eta * self.grad_w
        self.b -= eta * self.grad_b

#各層の初期化
middle_layer = MiddleLayer(n_in,n_mid)
output_layer = OutputLayer(n_mid,n_out)

#学習
sin_data = np.sin(np.pi * X)

for i in range(epoch):
    # インデックスをシャッフル
    index_random = np.arange(n_data)
    np.random.shuffle(index_random)

    #結果の表示用
    total_error = 0
    plot_x = []
    plot_y = []

    for idx in index_random:
        #入力
        x = input_data[idx:idx+1]\
        #正解
        t = correct_data[idx:idx+1]

        #順伝播
        middle_layer.forward(x.reshape(1,1))
        output_layer.forward(middle_layer.y)
        #逆伝播
        output_layer.backward(t.reshape(1,1))
        middle_layer.backward(output_layer.grad_x)

        #重みとバイアスの更新
        middle_layer.update(eta)
        output_layer.update(eta)

        if i%interval == 0:

            #行列をベクトルに戻す
            y = output_layer.y.reshape(-1)
            #二乗和誤差の計算
            total_error += - np.sum(t * np.log(y + 1e-7))
            #確率の大小を比較し、分類する
            if y[0] > y[1]:
                x_1.append(x[0])
                y_1.append(x[1])
            else:
                x_2.append(x[0])
                y_2.append(x[1])


    if i%interval == 0:

        #出力のグラフの表示
        plt.plot(X, sin_data, linestyle="dashed")
        plt.scatter(x_1, y_1, marker="+")
        plt.scatter(x_2, y_2, marker="x")
        plt.show()
        #エボック数と誤差の表示
        print("Epoch:" + str(i) + "/" + str(epoch)), "Error:" + str(total_error/n_data)
