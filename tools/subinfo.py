#encoding: utf-8

# to many string concatenation here, run with pypy

import sys

def buildngram(wd,n):
	lwd=len(wd)
	ngt="__ngram"+str(n)+"__"
	prs=[wd[ind:ind+n] for ind in xrange(lwd-n+1)]
	rs=[ngt+u for u in prs]
	return rs, prs

def buildunig(wd):
	return ["__char__"+wdu for wdu in wd]

def colngrams(wd):
	rs=buildunig(wd)
	lwd=len(wd)
	ngc=[]
	if lwd>2:
		for i in xrange(2, lwd):
			ng,png=buildngram(wd, i)
			rs.extend(ng)
			for ngu,pngu in zip(ng,png):
				tmp=["__combine__",ngu]
				tmp.extend(buildunig(pngu))
				ngc.append(" ".join(tmp))
				lng=len(pngu)
				if lng>2:
					for j in xrange(2, lng):
						ngg, _=buildngram(pngu, j)
						tt=["__combine__",ngu]
						tt.extend(ngg)
						ngc.append(" ".join(tt))
	return rs, ngc

def buildsubinfocore(unit):
	ind=unit.rfind("/")
	wd=unit[:ind]
	tag="__pos__"+unit[ind+1:]
	rs=["__combine__",wd,tag]
	wdc, subc = colngrams(wd)
	rs.extend(wdc)
	rs=[" ".join(rs)]
	rs.extend(subc)
	return "\n".join(rs)

def buildsubinfo(tlin):
	rs=[]
	for lu in tlin:
		rs.append(buildsubinfocore(lu))
	return "\n".join(rs)

def handle(srcf,rsf):
	with open(rsf,"w") as fwrt:
		with open(srcf) as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=tmp.decode("utf-8")
					wd, txt=tmp.split("	")
					fwrt.write(buildsubinfo(txt.split(" ")).encode("utf-8"))
					fwrt.write("\n".encode("utf-8"))

if __name__=="__main__":
	handle(sys.argv[1].decode("utf-8"),sys.argv[2].decode("utf-8"))
