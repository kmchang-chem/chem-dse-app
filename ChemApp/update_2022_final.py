import pandas as pd

# 2022 DSE Paper 1A Answers & Explanations
# Mapping User's List (35=Q1) to our CSV IDs
# 35.C 36.C 37.A 38.B 39.C 40.B 41.D 42.C 43.C 44.A
# 45.C 46.D 47.B 48.B 49.C 50.D 51.A 52.D 53.D 54.C
# 55.A 56.D 57.A 58.C 59.B 60.D 61.A 62.B 63.B 64.A
# 65.B 66.A 67.D

updates = {
    35: ("C", "Adding marble ($CaCO_3$) to water does not produce $CO_2$ because calcium carbonate is insoluble in water. You need an acid to react with marble."),
    36: ("C", "Vanadium (V) is element 23 (23 protons). Mass number 51 means neutrons = $51 - 23 = 28$. For $V^{3+}$ ion, electrons = $23 - 3 = 20$. Answer: 28, 20."),
    37: ("A", "Sodium chloride ($NaCl$) is an ionic compound. It dissociates into ions in solution or molten state, conducting electricity. $SiO_2$ is covalent network, methanol is molecular, mercury is a metal (electronic conductor)."),
    38: ("B", "You should Rinse the pipette with the solution to be delivered (to prevent dilution). However, you should NEVER rinse the conical flask with the solution. This adds extra moles of analyte, causing a positive error."),
    39: ("C", "Element X forms $XH_4^+$. This is analogous to ammonium ($NH_4^+$). Since H is +1, X must have 5 valence electrons to form 4 bonds and have a +1 charge (or coordinate bond). X is in Group V."),
    40: ("B", "Reaction: $3Cu^{2+} + 2PO_4^{3-} \\rightarrow Cu_3(PO_4)_2$. Moles $Cu$ = 0.04, $PO_4$ = 0.02. Stoichiometry requires 1.5x moles of Cu for every PO4. $0.02 \\times 1.5 = 0.03$ mol Cu needed. We have 0.04. Remaining $Cu^{2+} = 0.04 - 0.03 = 0.01$ mol."),
    41: ("D", "White solid insoluble in water? (Exclude $MgSO_4$, $Pb(NO_3)_2$). Insoluble in excess $NH_3$? $Zn(OH)_2$ dissolves in excess $NH_3$ (complex ion). $CaCO_3$ is insoluble in both."),
    42: ("C", "The structure shown is PMMA (Perspex). Monomer is methyl 2-methylpropenoate. It contains a C=C double bond, so it undergoes addition polymerisation."),
    43: ("C", "Solubility in water depends on Hydrogen Bonding. Y (Ethane-1,2-diol) has 2 -OH groups (Most soluble). Z (Methyl ethanoate) is a polar ester (Moderate). X (Butan-1-ol) has large hydrophobic chain (Least soluble relative to Z?). *Correction*: Esters like Z are soluble, but alcohols like X are also soluble. However, Y is miscible. The correct order given by key is Y > Z > X."),
    44: ("A", "$Zn + 2Ag^+ \\rightarrow Zn^{2+} + 2Ag$. Moles $Ag^+$ = 0.1, $Zn$ = 0.1. Ratio 1:2. 0.1 mol $Ag^+$ needs 0.05 mol $Zn$. We have 0.1 mol $Zn$. So $Zn$ is in excess, $Ag^+$ is limiting (0 remains). Result: Some Zn reacted, No Ag+ remains."),
    45: ("C", "Electrolysis of $CuSO_4$ with Cu cathode and C anode. Cathode ($Cu^{2+} + 2e \\rightarrow Cu$): Copper deposited. Anode ($4OH^- \\rightarrow O_2 + ...$): Oxygen gas formed because Carbon is inert."),
    46: ("D", "Balancing $xNH_3 + yO_2 \\rightarrow xNO + zH_2O$. N: x=x. H: 3x=2z. O: 2y=x+z. Try x=4. Then z=6. 2y=4+6=10, so y=5. Coefficients: 4, 5, 6."),
    47: ("B", "Left beaker ($I^-$) is Anode (Oxidation: $2I^- \\rightarrow I_2 + 2e^-$). Brown color $I_2$ appears. Right beaker ($Fe^{3+}$) is Cathode (Red: $Fe^{3+} \\rightarrow Fe^{2+}$)."),
    48: ("B", "Hess Law: $\\Delta H = 2 \\times \\Delta H_f(NaOH) - [\\Delta H_f(Na_2O) + \\Delta H_f(H_2O)]$. $\\Delta H = 2(-425) - [-414 + (-286)] = -850 - (-700) = -150$ kJ."),
    49: ("C", "HCl reaction: P (no gas) < Q, R. So P is least reducing (least reactive). Zn reaction: Zn reacts with chlorides of P, Q (so Zn > P, Q) but not R (so R > Zn). Order: $P < Q < R$."),
    50: ("D", "Product is a tri-bromo compound. X had 1 double bond + 1 Br. Reaction adds 2 Br. Total 3 Br. Options (2) and (3) fit the structure logic."),
    51: ("A", "Set-up is Simple Distillation. (1) Desalination (water from salt) - Yes. (2) Diesel is a mix, propane is gas - No. (3) Liquid air components have close boiling points - Need Fractional Distillation."),
    52: ("D", "(1) Cu + HCl: No reaction. (2) Fe + H2SO4: $Fe + 2H^+ \\rightarrow Fe^{2+} + H_2$. (3) Ca + NaOH: Ca reacts with water in the solution ($Ca + 2H_2O \\rightarrow Ca(OH)_2 + H_2$). So (2) and (3)."),
    53: ("D", "Structures comparison. (2) Same molecular formula? Count C,H. Yes. (3) Insoluble? Large hydrocarbon parts. Yes."),
    54: ("C", "Na + Water. (1) Moves quickly (Exothermic/Gas propels). (2) Red color? No, alkali turns Universal Indicator Blue/Purple. (3) Exothermic? Yes. Answer (1) and (3)."),
    55: ("A", "(1) $\\Delta H_f$ of element (Graphite) is 0. (2) Combustion is always exothermic (-ve). (3) $\\Delta H_f(CO) = C + 0.5 O_2$. Combustion $C + O_2$. Not equal."),
    56: ("D", "pH 1 vs 3. (1) A has more $H^+$, likely stronger. (2) B is weaker, partial dissociation, so molecules present. (3) Monobasic acids, same Vol, same Conc = Same Moles. NaOH neutralizes total moles. Yes."),
    57: ("A", "Fractionating Tower. S is lower/hotter than Q. (1) S darker? Yes. (2) R (lower than P) more viscous? Yes. (3) Q (lower than P) more flammable? No, volatility decreases down."),
    58: ("C", "1st: Combustion enthalpy depends on mole size (C2 vs C4). False. 2nd: Ethene ($C_2H_4$) and Butene ($C_4H_8$) both have empirical formula $CH_2$. True."),
    59: ("B", "Let $CH_4 = x$, $C_2H_6 = 50-x$. $CO_2$ produced: $1(x) + 2(50-x) = 80$. $x + 100 - 2x = 80$. $x = 20$. Methane is 20 $cm^3$."),
    60: ("D", "Curve Y has lower initial rate (less steep) but same final amount (same plateau). Using 'Granules' instead of 'Powder' decreases surface area (slower rate) but same mass (same yield)."),
    61: ("A", "Cis-trans: Needs C=C with diff groups. Enantiomerism: Needs chiral carbon. The structure likely lacks these features based on answer A."),
    62: ("B", "Graph: X drops from 1.2 to 0.8 (Change 0.4). Y rises from 0 to 1.2 (Change 1.2). Ratio 1:3. Equation: $X \\rightleftharpoons 3Y$."),
    63: ("B", "Hydrolysis of amide. NaOH gives carboxylate salt. Adding excess HCl converts it to Carboxylic Acid (COOH) and Ammonium/Amine salt."),
    64: ("A", "$K_c = [SO_3]^2 / ([SO_2]^2 [O_2])$. Eqm moles: $SO_3=0.3$. $SO_2=0.4-0.3=0.1$. $O_2=0.6-0.15=0.45$. Vol=1. $K_c = 0.3^2 / (0.1^2 \\times 0.45) = 0.09 / 0.0045 = 20$."),
    65: ("B", "Set up measures gas volume. (1) Acid-Base (No gas). (2) Metal + Acid (H2 gas). (3) Displacement (No gas). Only (2) works."),
    66: ("A", "Transition metal characteristics: (1) Colored ions (Orange) - Yes. (2) Eqm shift - General property. (3) Ox states - Here both +6. Demonstrates 'Variable' only if they were different. Answer (1) only."),
    67: ("D", "Aspirin. (1) Ester group - Yes. (2) Medical use - Yes. (3) Soluble in $Na_2CO_3$ - Yes, because it has a -COOH group which reacts to form a soluble salt.")
}

try:
    df = pd.read_csv("questions.csv", encoding="utf-8")

    count = 0
    for q_id, (ans, exp) in updates.items():
        mask = df['id'] == q_id
        if mask.any():
            df.loc[mask, 'correct_answer'] = ans
            df.loc[mask, 'explanation'] = exp
            count += 1

    df.to_csv("questions.csv", index=False, encoding="utf-8")
    print(f"✅ 成功更新了 {count} 題的答案與詳解 (Q1-Q33)！")

except Exception as e:
    print(f"❌ 錯誤: {e}")