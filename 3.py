import matplotlib.pyplot as plt
import math
import numpy as np

def read_file(name):
	file = open(name+'.csv', 'r')
	data = file.read().strip().split('\n')
	data = data[2:]
	t, Q0, Q, P= [], [], [], []
	for line in data:
		elements = line.split(',')
		t.append(float(elements[0]))
		Q0.append(float(elements[1])*10**-6)
		Q.append(float(elements[2])*10**-6)
		P.append(float(elements[3])*10**5)
	return t, Q0, Q, P

def plotter(x, y, x_label, name):
	linestyle=['solid', 'dotted', 'dashed', 'dashdot', (0, (5,10)), (0, (5,1)), (0, (3,10,1,10)), (0, (3,1,1,1))]
	for i in range(len(y)):
		plt.plot(x, y[i], label = name[i], linestyle=linestyle[i])
	plt.title(name[0])
	if len(name)>1:
		plt.legend(loc='best')
	plt.grid()
	plt.ylabel(str(name[0]))
	plt.xlabel(x_label)
	plt.tight_layout()
	plt.savefig(str(name[0])+str('.png'))
	plt.close()

t, Q0, Q, P = read_file('3')
tau1 = 5000
tau2 = 1000
P_der_Q, exp_P_der_Q, log_t, PdQ_fit = [], [], [], []
for i in range(len(P)):
	P_der_Q.append(P[i]/(Q0[i]-Q[i]))	#dPc/(Q0-Q))=1/(4 pi eps)*(lnt+ln2.25*psi/rc**2)
	log_t.append(math.log(t[i]))
lenght = len(t)//8*7
k, b = np.polyfit(log_t[lenght:], P_der_Q[lenght:], 1)	#k=1/(4 pi eps), b=1/(4 pi eps) ln (2.25psi/rc**2)
for i in range(len(t)):
	PdQ_fit.append(k*log_t[i]+b)
eps = 1/(4*3.14*k)
hiStar_rc2 = math.exp(b*4*3.14*eps)/2.25
hi_rc2 = hiStar_rc2*(tau1+tau2)/tau1

plotter(t, [P], r'$t$ [s]', [r'$dP_c$($t$) [Pa]'])
plotter(log_t[lenght:], [P_der_Q[lenght:], PdQ_fit[lenght:]], r'$ln(t)$', [r'$\frac{dP_c(t)}{Q_0-Q(t)}$', 'fit, k='+str(round(k,2))+' b='+str(round(b,2))])
print(eps, 'epsilon [m^3/Pa*s]')
print(hiStar_rc2, 'hi*/r_c^2 [1/s]')
print(hi_rc2, 'hi/r_c^2 [1/s]')