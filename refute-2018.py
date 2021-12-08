#!/usr/bin/env python
# coding: utf-8

## The code for Trybus A., Some Remarks on Implementing Refutation Systems.

import re
#import itertools
import random

def check_membership(y,X):
	for x in X:
		if y in x:
			return True
	return False



def preprocess(X):
	new_X = []
	for x in X:
		new_x = x.split('.')
		new_x = [value for value in new_x if value != '']
		checked = []
   		for e in new_x:
       			if e == 'D' or e == 'C':
           			checked.append(e)
			else:
				if '.'+e+'.' not in checked:
					checked.append('.'+e+'.')
   			
		new_X.append(checked)
	joined_X = []
	for x in new_X:
		joined_x = ''.join(x)
		joined_X.append(joined_x)
	return joined_X


# leaves only one copy of a given formula in a set

def preprocess_set(X):
	new_X = []
	for x in X:
		if x not in new_X:
			new_X.append(x)
	return new_X

# X conjunction of disjunctions
# Y disjunction of conjunctions
# changes Y into Y' which is of the same form as X
# Y' conjunction of disjunctions

def oneside_normal_form(Y):
	#print Y
	Y_prime = []
	for i in Y:
		if len(i) > 2 and i != '.1.' and i != '.0.':
			all_elements = re.findall(r'\.[A-Za-z0-9]+\.',i[1:])
		
			i_prime = 'D'
			for a in all_elements:
				a = a[1:-1]
				a_prime = ''
			
				if a[0] == 'N':
				
					a_prime = '.'+a[1:]+'.'
				elif a == '0':
					a_prime = '.1.'
				elif a == '1':
					a_prime = '.0.'
			
				else:
				
					a_prime = '.N'+a+'.'
			
				i_prime = i_prime+a_prime
			Y_prime.append(i_prime)
		elif len(i) == 1 and i == 'C':
			Y_prime.append('.0.')
		elif i == '.1.':
			Y_prime.append('.0.')
		elif i == '.0.':
			Y_prime.append('.1.')
		else:
			print 'Exception caught in oneside_normal_form'
	return Y_prime

def rev_oneside_normal_form(Y_Prime):
	Y = []
	for i in Y_Prime:
		if len(i) > 2 and i != '.1.' and i != '.0.':		
			all_elements = re.findall(r'\.[A-Za-z0-9]+\.',i[1:])
		
			i_rev = 'C'
			for a in all_elements:
				a = a[1:-1]
				a_rev = ''
				
				if a[0] == 'N':
				
					a_rev = '.'+a[1:]+'.'
				elif a == '0':
					a_rev = '.1.'
				elif a == '1':
					a_rev = '.0.'		
				else:
					
					a_rev = '.N'+a+'.'
			
				i_rev = i_rev+a_rev
			Y.append(i_rev)

		elif len(i) == 1 and i == 'D':
			Y.append('.1.')
		elif i == '.0.':
			Y.append('.1.')	
		elif i == '.1.':
			Y.append('.0.')		
		else:
			print 'Exception caught in rev_oneside_normal_form'
	return Y

#checks if formulas are the same disregarding the order of the elements

def equal_formulas(a,b):
	all_lit_a = re.findall(r'\.[A-Za-z]+\.',a[1:])
	all_lit_b = re.findall(r'\.[A-Za-z]+\.',b[1:])
	if a[0] == b[0]:
		for alla in all_lit_a:
			for allb in all_lit_b:
				if alla not in all_lit_b or allb not in all_lit_a:
				 	return False
		return True
	else: return False

#gathers literals of size 1 (negates them or gets rid of negation) and cuts of the leading connective for further processing			

def gather_singles(A):
	singles = []
	for a in A:
		if len(a) < 6:
			singles.append(a[1:])
	return singles
	
#takes all the singles and produces all possible combinations of these


def sum_up(A):
	singles = gather_singles(A)
	combinations = []
	i = 2
	while i < len(singles)+1:
		value = [list(x) for x in itertools.product(singles,repeat=i)]
		for v in value:	
			va = ''.join(v)
			combinations.append(va)
		i = i+1
	final = preprocess(combinations)
	return final



def same_formulas(new_X,new_Y):
	X_lit = sum_up(new_X)
	Y_lit = sum_up(new_Y)
	Y_prime = oneside_normal_form(new_Y)
	for i in range(0,len(X_lit)):
		X_lit[i] = 'C'+X_lit[i]

	for i in range(0,len(Y_lit)):
		Y_lit[i] = 'D'+Y_lit[i]

	for x in new_X:
		for y in Y_prime + Y_lit:
			if equal_formulas(x,y):
				return x
	for y in gather_singles(new_Y):
		for x in gather_singles(new_X):
			if y == x:
				return y
	return False

#given a set of formulas, it extracts all the variables used

def variable_search(LitSet):
	var = []
	for i in LitSet:
		all_lit_i = re.findall(r'\.[A-Za-z]+\.',i[1:])
		for l in all_lit_i:
			if l[1] == 'N':
				if l[2] not in var:
					var.append(l[2])
			else:
				#print 'error'
				if l[1] not in var:
					var.append(l[1])
				#if 'D' in l or 'C' in l:
				#	print 'error'
	
	return var			

# produces all the formulas containing given literal
def literal_search(var,LitSet):
	lits = {}
	for v in var:
		lits[v] = []
		lits['N'+v] = []
		for i in LitSet:
			if 'N'+v+'.' in i:
				lits['N'+v].append(i)
			if '.'+v+'.' in i:
				lits[v].append(i)
	#for key in lits:
    	#	for k in lits[key]:
	#		print 'hello'
	return lits
#splits a clause into two: one is a single variable or its negation and the other is the rest 

def take_out(x,clause):
	new_clause = [clause[0]]
	result = ''
	all_lit = re.findall(r'\.[A-Za-z0-9]+\.',clause[1:])
	news = [value for value in all_lit if value != '.'+x+'.']
	new_clause = new_clause+news
	result = ''.join(new_clause)
	return result


# removes all occurences of a formula from a given set of formulas

def take_out_fla(fla, flas):
	news = [value for value in flas if value != fla]
	return news

# checks whether two formulas share at least one variable:

def vars_in_common(X,Y):
	var1 = variable_search(X)
	var2 = variable_search(Y)
	for x in var1:
		for y in var2:
			if x == y:
				return True
	
	return False
	#return any(x in set_v1 for x in var2)

## the main function, given two formulas one a conjunction of DNFs and the other a disjunction of CNFs, it produces an interpolant of these, if it exists (pseudo-randomly selecting the literals to be eliminated)

def refute(X,Y):
	# the following two lines,uncommented, help build a search tree:
	print 'X: ',X
	print 'Y: ',Y
	
	
	if vars_in_common(X,Y):
		new_X = X
		new_Y = Y
		Y_Prime = oneside_normal_form(new_Y)
		var = variable_search(new_X+Y_Prime)
		Remainder_x = []
		Remainder_y = []
		selected = []
		literals_X = literal_search(var,new_X)
		literals_Y_Prime = literal_search(var,Y_Prime)
		total_literals = {}
		if len(literals_X) != 0:
			for key in literals_X:	
				if key in literals_Y_Prime:
	
					total_literals[key] = literals_X[key]+literals_Y_Prime[key]
				else:
					total_literals[key] = literals_X[key]
			if len(literals_Y_Prime) != 0:
				for key in literals_Y_Prime:
					if key not in total_literals:
						total_literals[key] = literals_Y_Prime[key]
			for key in total_literals:
				if 'N' not in key:
					if len(total_literals[key]) != 0 and len(total_literals['N'+key]) != 0:
						selected.append(key)




		if len(selected) != 0:
			chosen_literal = random.choice(selected)

			Remainder_x = new_X
			Remainder_y = Y_Prime
			for i in literals_X[chosen_literal]:	
				Remainder_x = take_out_fla(i, Remainder_x)

			for i in literals_Y_Prime[chosen_literal]:
				Remainder_y = take_out_fla(i, Remainder_y)
 
			for i in literals_X['N'+chosen_literal]:	
				Remainder_x = take_out_fla(i, Remainder_x)

			for i in literals_Y_Prime['N'+chosen_literal]:		
				Remainder_y = take_out_fla(i, Remainder_y)

			X_f1 = literals_X[chosen_literal]

			XF1 = []
			for xf1 in X_f1:
				xf1_new = take_out(chosen_literal,xf1)
				if xf1_new != 'D':
					XF1.append(xf1_new)
				else:
					XF1.append('.0.')

			Y_Prime_f1 = literals_Y_Prime[chosen_literal]
			YPF1 = []
			for ypf1 in Y_Prime_f1:
				ypf1_new = take_out(chosen_literal,ypf1)
				if ypf1_new != 'D':
					YPF1.append(ypf1_new)
				else:
					YPF1.append('.0.')

			X_f2 = literals_X['N'+chosen_literal]
			XF2 = []
			for xf2 in X_f2:
				xf2_new = take_out('N'+chosen_literal,xf2)
				if xf2_new != 'D':
					XF2.append(xf2_new)
				else:
					XF2.append('.0.')		
			Y_Prime_f2 = literals_Y_Prime['N'+chosen_literal]
			YPF2 = []
			for ypf2 in Y_Prime_f2:
				ypf2_new = take_out('N'+chosen_literal,ypf2)
				if ypf2_new != 'D':
					YPF2.append(ypf2_new)
				else:
					YPF2.append('.0.')

			YF1 = rev_oneside_normal_form(YPF1 + Remainder_y)
			YF2 = rev_oneside_normal_form(YPF2 + Remainder_y)
			XF1 = XF1 + Remainder_x
			XF2 = XF2 + Remainder_x
			F1 = (XF1, YF1)
			F2 = (XF2, YF2)
			print 'The literal is ',chosen_literal
			#print F1, F2
			return refute(XF1,YF1),refute(XF2,YF2)




			



		elif len(selected) == 0:
			print 'no literals in common'
			#print X, Y
			return X, Y
			
	else:
		print 'no vars in common'
		#print X, Y
		return X, Y

#refute(['D.r..p.', 'D.Nr..p..s.', 'D.s..t.'],['C.Nr..Nq.', 'C.Nt..Nq.']) # Ex1
#refute(['D.r..p.', 'D.Nr..Np..s.', 'D.s..t.'],['C.Nr..Nq.', 'C.Nt..Nq.']) # Ex2
#refute(['D.p..Ns.', 'D.q..r.', 'D.Np..Nq.','D.Nr..s.'],['C.Np..q.','C.p..Nq.']) # Ex3 

