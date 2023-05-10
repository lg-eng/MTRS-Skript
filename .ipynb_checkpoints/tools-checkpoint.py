from sympy import *
from sympy.physics.units.systems import SI
from sympy.physics.units import Quantity, length, mass, time, Dimension
from sympy.physics.units import day, gravitational_constant as G
from sympy.physics.units import meter, kilogram, second, hz

from IPython.display import Markdown as md

class tools:
    
    def __init__(self):
        self.define_symbols()
        #print(self.sym_legend)

    def assign_legend_entry(self,symbol,entry):
        try:
            self.sym_legend[symbol] = entry
        except:
            self.sym_legend = self.sym_legend | {symbol:entry}
            
    def assign_unit_entry(self,symbol,entry):
        try:
            self.sym_unit[symbol] = entry
        except:
            self.sym_unit = self.sym_unit | {symbol:entry}
    
    def show_numerical_value(self,vals,symbol):
        #display(float(vals[symbol]))
        #display(Latex(' ' + latex(symbol) + ' = '))
        text_template = ' %.2e'
        #display(Latex(' ' + latex(symbol) + '  =  \\textrm{' + (text_template % vals[symbol]) + '}' ) )   
        #display(Eq(symbol,vals[symbol].evalf()))

    def show_legend_entry(self,symbol):
        display(Latex(' ' + latex(symbol) + '  ...  \\textrm{' + self.sym_legend[symbol] + '}' ) )


    def define_symbols(self):
        self.sym_legend = {}
        self.sym_unit = {}

        self.t,self.f = symbols(r't,f',real=true)
        self.assign_legend_entry(self.t,'Zeit')
        SI.set_quantity_dimension(self.t, time)
        self.assign_unit_entry(self.t,second)
        
        self.assign_legend_entry(self.f,'Frequenz')
        SI.set_quantity_dimension(self.f, 1/time)
        self.assign_unit_entry(self.f,hz)
        
        self.T = symbols(r'T',real=true)
        self.assign_legend_entry(self.T,'Periodendauer')
        SI.set_quantity_dimension(self.T, time)
        self.assign_unit_entry(self.T,second)
        
    
        

