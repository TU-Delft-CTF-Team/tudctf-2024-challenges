from Crypto.Util.number import long_to_bytes
import gmpy2

n = 21701276789703566112504440205277555500980530128986359518040085238579492008664491239779343518584422229077053517904889879774432012669255189182767093071015636540803807369329816017210955271052100748418252739123022642466971997293254385715250893895562550386267802102393722102960888248315499433915933167111353820754212286044222761230587787537381114214629345548673470876451909280754526473267634962770016896202653419146606810191084200373895628231943729524778860390643353550217471116322166950691588543208724312794723891297282096470388516139442635828642963504323602485358541379911080919655531217735499904968521675633464510356279
e = 3
ct = 41755248204404130616299001100754028765169384749909228662216774048159964962657804814776133421743783302115983347982451417399364688492589409641493317159343846814738353341705032427144641017478145125

pt, is_exact = gmpy2.iroot(ct, 3)
# assert is_exact
print(long_to_bytes(pt).decode())