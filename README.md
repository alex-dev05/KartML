# KartML
Machine Learning project using Reinforcement Learning algorithms to learn an agent how to drive a kart


Data Flow

code for  https://www.websequencediagrams.com/

title Machine Learning

Unity->Python: FlaskAPI
note right of Unity: Game start, Collecting data from unity
Python->Unity: FlaskAPI 
note right of Python: Predict using Model

![image](https://user-images.githubusercontent.com/37021205/152438475-e74e1dd2-1d45-4f22-b600-e8c3b94291a2.png)


Collecting Data

Pentru inceput, s-a rulat jocul in mod normal, kartul fiind controlat prin intermediul sagetilor de pe tastatura (up arrow, donw arrow, left arrow respectiv right arrow). Datele colectate din mediul Unity au fost salvate intr-un fisier csv. Pentru fiecare sesiune de joc se creaza un astfel de fisier (vezi folderul Exports). S-au merge-uit 5 astfel de fisiere si s-a obtinut un fiser mai mare.

Fisierul respectiv a fost curatat in python si asupra lui s-a folosit un algoritm de clasificare care returna o valoarea de la 0 la 15.
Valoarea respectiva reprezinta combinatiile posibile pe care kart-ul le poate avea ca si input:
val = 0 -> up arrow = apasat, down arrow = apasat, left arrow = apasat, rigth arrow = apasat
val = 1 -> up arrow = apasat, down arrow = apasat, left arrow = apasat, rigth arrow = nu e apasat
....
val = 15 -> up arrow = nu e apasat, down arrow = nu e apasat, left arrow = nu e apasat, rigth arrow = nu e apasat

In momentul in care incepe jocul in modul "NPC", la fiecare frame cand se executa functia de update, se face un call la functia din Python prin intermediul API-ului de tip FLask printr-un request de tip post, care contine datele colectate din mediul unity, si returneaza ca si response valoarea de mai sus.
Valoarea respectiva este interpretata si se da comanda catre unity prin intermediul Vertical si Horizontal.


Vertical ia valori intre -1 si 1.
-1 -> down arrow apasat
0 -> down arrow/up arrow neapasate
1 - up arrrow apasat

Vertical ia valori intre -1 si 1.
-1 -> left arrow apasat
0 -> left arrow/ right arrow neapasate
1 - right arrrow apasat
