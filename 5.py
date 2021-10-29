import matplotlib.pyplot as plt
import math
import numpy as np

def read_file(name):
	file = open(name+'.csv', 'r')
	data = file.read().strip().split('\n')
	data = data[2:]
	output = [[], [], [], []]
	for line in data:
		elements = line.split(',')
		for i in range(len(elements)):
			output[i].append(float(elements[i]))
	return output

def plotter(x, y, x_label, name):
	linestyle=['solid', 'dotted', 'dashed', 'dashdot', (0, (5,10)), (0, (5,1)), (0, (3,10,1,10)), (0, (3,1,1,1))]
	for i in range(len(y)):
		plt.plot(x, y[i], label=name[i],linestyle=linestyle[i])
	plt.title(name[0]+'&'+name[1])
	plt.grid()
	plt.legend(loc='best')
	# plt.ylabel(str(name))
	plt.xlabel(x_label)
	plt.tight_layout()
	plt.savefig(str(name)+str('.png'))
	plt.close()

def find_max(func):
	t_qmax= []
	func0=max(func)
	for i in range(len(func)):
		if func[i] == func0:
			t_qmax.append(t[i])
	return func0, t_qmax

r = 420
gamma = 1.781
t, q, Pc, Pr = read_file('5')
for i in range(len(t)):
	q[i] = q[i]*10**-6
	Pc[i] = Pc[i]*10**5
	Pr[i] = Pr[i]*10**5

deltaT=[]
q0, t_qmax = find_max(q)
for i in range(len(t_qmax)-1):
	deltaT.append(t_qmax[i+1]-t_qmax[i])

t_Pcmax = find_max(Pc)[1]
t_Pcmax_av = sum(t_Pcmax)/len(t_Pcmax)
delta_qc = 6.28*(t_Pcmax_av-t_qmax[0])/deltaT[0]

Pr0, t_Prmax = find_max(Pr)
t_Prmax_av = sum(t_Prmax)/len(t_Prmax)
delta_qr = 6.28*(t_Prmax_av-t_qmax[0])/deltaT[0]

hi = 3.14*r**2/(deltaT[0]*(delta_qr-3.14/8)**2)
eps = q0/(2**(7/2)*3.14**0.5*Pr0)*math.exp(-(delta_qr-3.14/8))/(delta_qr-3.14/8)**0.5
rc = r*2**0.5/gamma*math.exp(-3.14/(4*math.tan(delta_qc)))/(delta_qr-3.14/8)

lenght = 0
plotter(t[lenght:], [Pr[lenght:], Pc[lenght:]], r'$t$ [s]', [r'$P_r$($t$) [Pa]', r'$P_c$($t$) [Pa]'])
print(q0, 'q0')
print(t_qmax, 't при q0')
print(deltaT, 'Период колебаний T')
print(delta_qr, 'Разность фаз дебит-давление [rad]')
print(hi, 'hi [m^2/s]')
print(eps, 'eps [m^3/(Pa*s)]')
print(rc, 'rc [m]')