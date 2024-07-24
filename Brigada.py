doprava_zauceni = 100
plat_zauceni = 200
cas_zauceni = 1.5
cas_zauceni_doprava = 2

doprava_prace = 0
plat_prace = 180
cas_prace = 10
cas_doprava_prace = 0.5




cena = 2*( 2*doprava_zauceni) + 2*doprava_prace
hrubej_zisk = ( plat_zauceni * cas_zauceni )*2 + cas_prace*plat_prace
cistej_zisk = hrubej_zisk - cena
kc_na_hodinu = cistej_zisk+200 / (2 * ( 2*cas_zauceni_doprava + cas_zauceni ) + 2 * cas_doprava_prace + cas_prace )

print(f' cena={cena}, Hrubej zisk={hrubej_zisk}, cistej zisk={cistej_zisk}, kc/h={kc_na_hodinu}')
