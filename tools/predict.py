#encoding: utf-8

import sys

from math import sqrt

def ldvec(vecf):
	rsd = {}
	cv = {}
	unkv = False
	with open(vecf) as frd:
		for line in frd:
			tmp = line.strip()
			if tmp:
				tmp = tmp.decode("utf-8")
				ind = tmp.find(" ")
				key = tmp[:ind]
				value = tuple(float(tmpu) for tmpu in tmp[ind+1:].split(" "))
				if key == "<unk>":
					unkv = value
				else:
					if key.startswith("__label__"):
						cv[key] = norm_vec(value)
					else:
						rsd[key] = value					
	if not unkv:
		unkv = (0.0 for i in xrange(len(rsd[rsd.keys()[0]])))
	return rsd, cv, unkv

def add_vec(v1, v2):
	return tuple(v1u + v2u for v1u, v2u in zip(v1, v2))

def mul_vec(v1, v2):
	return tuple(v1u * v2u for v1u, v2u in zip(v1, v2))

def dot_vec(v1, v2):
	return sum_vec(mul_vec(v1, v2))

def sum_vec(vl):
	sum = 0
	for vu in vl:
		sum += vu
	return sum

def norm_vec(vl):
	s = dot_vec(vl, vl)
	if s > 0:
		s = sqrt(s)
		return tuple(vu/s for vu in vl)
	else:
		return vl

def sentvec(lin, vd, unkv):
	rs = False
	for lu in lin:
		if not rs:
			rs = vd.get(lu, unkv)
		else:
			rs = add_vec(rs, vd.get(lu, unkv))
	return rs

def sentvecnounk(lin, vd):
	rs = False
	for lu in lin:
		if not rs:
			if lu in vd:
				rs = vd[lu]
		else:
			if lu in vd:
				rs = add_vec(rs, vd[lu])
	return rs

def g_class(svec, classes):
	norm_svec = norm_vec(svec)
	rs = ""
	rscore = -1.1
	for k, vc in classes.iteritems():
		curscore = dot_vec(vc, norm_svec)
		if curscore > rscore:
			rscore = curscore
			rs = k
	return rs, rscore

def handle(srcf, rsf, vecf, useunk):
	vecs, cls, unkv = ldvec(vecf)
	with open(srcf) as frd:
		with open(rsf, "w") as fwrt:
			for line in frd:
				tmp = line.strip()
				if tmp:
					if useunk:
						tmp = sentvec(tmp.decode("utf-8").split(" "), vecs, unkv)
					else:
						tmp = sentvecnounk(tmp.decode("utf-8").split(" "), vecs)
					tmp, score = g_class(tmp, cls)
					fwrt.write(tmp.encode("utf-8"))
					fwrt.write("\n".encode("utf-8"))

if __name__=="__main__":
	if len(sys.argv>4):
		handle(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"), sys.argv[3].decode("utf-8"), sys.argv[4].decode("utf-8"))
	else:
		handle(sys.argv[1].decode("utf-8"), sys.argv[2].decode("utf-8"), sys.argv[3].decode("utf-8"), True)
