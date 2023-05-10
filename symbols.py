def define_symbols():
    sym_legend = {}
    #Complex symbols
    Uhcl,Urcl = symbols(r'\underline{U}_h(l),\underline{U}_r(l)',real=false)
    sym_legend = assign_legend_entry(sym_legend,Uhcl,'Komplexe hinlaufende Spannungswelle')
    sym_legend = sym_legendassign_legend_entry(sym_legend,Urcl,'Komplexe rücklaufende Spannungswelle')