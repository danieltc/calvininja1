import tweepy
import logging
import time
import random
import datetime
# tem um arquivo twitterauth.py na raiz com as variaveis contendo as credenciais de autenticacao. Ele ta no gitignore tambem.
import twitterauth

bcw = {
    1: "PERGUNTA 1. Qual é o fim principal do homem?\n\nRESPOSTA. O fim principal do homem é glorificar a Deus, e gozá-lo para sempre.\n\n\nReferências: Rm 11.36; 1Co 10.31; Sl 73.25-26; Is 43.7; Rm 14.7-8; Ef 1.5-6; Is 60.21; 61.3.",
    2: "PERGUNTA 2. Que regra deu Deus para nos dirigir na maneira de o glorificar e gozar?\n\nR. A Palavra de Deus, que se acha nas Escrituras do Velho e do Novo Testamentos, é a única regra para nos dirigir na maneira de o glorificar e gozar.\n\nRef. Lc 24.27, 44; 2Pe 3.2, 15-16; 2Tm 3.15-17; Lc 16.29-31; Gl 1.8-9; Jo 15.10-11; Is 8.20; Hb 1:1 comparado com Lc 1.1-4 e Jo 20.30-31.",
    3: "PERGUNTA 3. Qual é a coisa principal que as Escrituras nos ensinam?\n\nR. A coisa principal que as Escrituras nos ensinam é o que o homem deve crer acerca de Deus, o dever que Deus requer do homem.\n\nRef. Jo 5.39; 20.31; Sl 119.105; Rm 15.4; 1Co 10.11.",
    4: "PERGUNTA 4. Quem é Deus?\n\nR. Deus é espírito, infinito, eterno e imutável em seu ser, sabedoria, poder, santidade, justiça, bondade e verdade.\n\nRef. Jo 4.24; Ex 3.14; Sl 145.3; 90.2; Tg 1.17; Rm 11.33; Gn 17.1, Ap 4.8; Ex 34.6-7.",
    5: "PERGUNTA 5. Há mais de um Deus?\n\nR. Há só um Deus, o Deus vivo e verdadeiro.\n\nRef. Dt 6.4; 1Co 8.4; Jr 10.10; Jo 17.3.",
    6: "PERGUNTA 6. Quantas pessoas há na Divindade?\n\nR. Há três pessoas na Divindade: o Pai, o Filho e o Espírito Santo, e estas três são um Deus, da mesma substância, iguais em poder e glória.\n\nRef. Mt 3.16-17; 28.19; 2Co 13.13; Jo 1.1; 3.18; At 5.3-4; Hb 1.3; Jo 10.30.",
    7: "PERGUNTA 7. Que são os decretos de Deus?\n\nR. Os decretos de Deus são o seu eterno propósito, segundo o conselho da sua vontade, pelo qual, para sua própria glória, Ele predestinou tudo o que acontece.\n\nRef. Rm 11.36; Ef 1.4-6, 11; At 2.23; 17.26; Jo 21.19; Is 44.28; At 13.48; 1Co 2.7; Ef 3.10-11.",
    8: "PERGUNTA 8. Como executa Deus os seus decretos?\n\nR. Deus executa os seus decretos nas obras da criação e da providência.\n\nRef. Ap 4.11; Dn 4.35; Is 40.26; 14.26-27; 46.9-11; At 4.24.",
    9: "PERGUNTA 9. Qual é a obra da criação?\n\nR. A obra da criação é aquela pela qual, Deus fez todas as coisas do nada, no espaço de seis dias, e tudo muito bem.\n\nRef. Gn 1; Hb 11.3; Sl 33.9; Gn 1.31.",
    10: "PERGUNTA 10. Como criou Deus o homem?\n\nR. Deus criou o homem macho e fêmea, conforme a sua própria imagem, em conhecimento, retidão e santidade com domínio sobre as criaturas.\n\nRef. Gn 1.27-28; Cl 3.10; Ef 4.24; Rm 2.14-15; Sl 86-8.",
    11: "PERGUNTA 11. Quais são as obras da providência de Deus?\n\nR. As obras da providência de Deus são a sua maneira muito santa, sábia e poderosa de preservar e governar todas as suas criaturas, e todas as ações delas.\n\nRef. Sl 145.17; 104.10-24; Hb 1.3; Mt 10.29-30; Os 2.6.",
    12: "PERGUNTA 12. Que ato especial de providência exerceu Deus para com o homem no estado em que ele foi criado?\n\nR. Quando Deus criou o homem, fez com ele um pacto de vida, com a condição de perfeita obediência: proibindo-lhe comer da árvore da ciência do bem e do mal, sob pena de morte.\n\nRef. Gl 3.12; Gn 2.17.",
    13: "PERGUNTA 13. Conservaram-se nossos primeiros pais no estado em que foram criados?\n\nR. Nossos primeiros pais, sendo deixados à liberdade da sua própria vontade, caíram do estado em que foram criados, pecando contra Deus.\n\nRef. Rm 5.12; Gn 3.6.",
    14: "PERGUNTA 14. Que é pecado?\n\nR. Pecado é qualquer falta de conformidade com a lei de Deus, ou qualquer transgressão desta lei.\n\nRef. Tg 2.10; 4.17; 1Jo 3.4.",
    15: "PERGUNTA 15. Qual foi o pecado pelo qual nossos primeiros pais caíram do estado em que foram criados?\n\nR. O pecado pelo qual nossos primeiros pais caíram do estado em que foram criados foi o comerem do fruto proibido.\n\nRef. Gn 3.12-13; Os 6.7.",
    16: "PERGUNTA 16. Caiu todo o gênero humano pela primeira transgressão de Adão?\n\nR. Visto que o pacto foi feito com Adão não só para ele, mas também para sua posteridade, todo gênero humano que dele procede por geração ordinária, pecou nele e caiu com ele na sua primeira transgressão.\n\nRef. Gn 1.28; At 17.26; 1Co 15.21-22; Rm 5.12-14.",
    17: "PERGUNTA 17. Qual foi o estado a que a queda reduziu o gênero humano?\n\nR. A queda reduziu o gênero humano a um estado de pecado e miséria.\n\nRef. Rm 5.12.",
    18: "PERGUNTA 18. Em que consiste o estado de pecado em que o homem caiu?\n\nR. O estado de pecado em que o homem caiu consiste na culpa do primeiro pecado de Adão, na falta de retidão original e na corrupção de toda a sua natureza, o que ordinariamente de chama Pecado Original, juntamente com todas as transgressões atuais que procedem dele.\n\nRef. Rm 5.18-19; Ef 2.1-3; Rm 8.7-8; Sl 51.5.",
    19: "PERGUNTA 19. Qual é a miséria do estado em que o homem caiu?\n\nR. Todo o gênero humano pela sua queda perdeu comunhão com Deus, está debaixo da sua ira e maldição, e assim sujeito a todas as misérias nesta vida, à morte e às penas do Inferno para sempre.\n\nRef. Gn 3.8, 24; Ef 2.3; Rm 6.23; Mt 25.41-46.",
    20: "PERGUNTA 20. Deixou Deus todo o gênero humano perecer no estado de pecado e miséria?\n\nR. Tendo Deus, unicamente pela sua boa vontade desde toda a eternidade, escolhido alguns para a vida eterna, entrou com eles em um pacto de graça, para os livrar do estado de pecado e miséria, e trazer a um estado de salvação por meio de um Redentor.\n\nRef. Ef 1.4; Tt 1.2; 3.4-7; Jo 17.6.",
    21: "PERGUNTA 21. Quem é o Redentor dos escolhidos de Deus?\n\nR. O único redentor dos escolhidos de Deus é o Senhor Jesus Cristo que, sendo o eterno Filho de Deus, se fez homem, e assim foi e continua a ser Deus e homem em duas naturezas distintas, e uma só pessoa, para sempre.\n\nRef. 1Tm 2.5; Jo 1.14; Rm 9.5; Cl 2.9; Hb 13.8.",
    22: "PERGUNTA 22. Como Cristo, sendo o Filho de Deus, se fez homem?\n\nR. Cristo, o Filho de Deus, fez-se homem tomando um verdadeiro corpo, e uma alma racional, sendo concebido pelo poder do Espirito Santo no ventre da virgem Maria, e nascido dela, mas sem pecado.\n\nRef. Hb 2.14; Mt 26.38; Lc 2.52; 1.31, 35; Hb 4.15.",
    23: "PERGUNTA 23. Que funções exerce Cristo como nosso Redentor?\n\nR. Cristo, como nosso Redentor, exerce as funções de profeta, sacerdote e rei, tanto no seu estado de humilhação como no de exaltação.\n\nRef. At 3.22; Hb 5.5-6; Sl 2.6; Jo 1.49.",
    24: "PERGUNTA 24. Como exerce Cristo as funções de profeta?\n\nR. Cristo exerce as funções de profeta, revelando-nos, pela sua Palavra e pelo seu Espírito, a vontade de Deus para a nossa salvação.\n\nRef. Jo 1.18; Hb 1.1-2; Jo 14.26; 16.13.",
    25: "PERGUNTA 25. Como exerce Cristo as funções de sacerdote?\n\nR. Cristo exerce as funções de sacerdote, oferecendo-se a si mesmo uma vez em sacrifício, para satisfazer a justiça divina, reconciliar-nos com Deus e fazendo contínua intercessão por nós.\n\nRef. Hb 9.28; Rm 3.24-26; 10.4; Hb 2.17; 7.25; Is 53.12.",
    26: "PERGUNTA 26. Como exerce Cristo as funções de rei?\n\nR. Cristo exerce as funções de rei, sujeitando-nos a si mesmo, governando-nos e protegendo-nos, contendo e subjugando todos os seus e os nossos inimigos.\n\nRef. Sl 110.3; At 2.36; 18.9-10; Is 9.6-7; 1Co 15.26-27.",
    27: "PERGUNTA 27. Em que consistiu a humilhação de Cristo?\n\nR. A humilhação de Cristo consistiu em Ele nascer, e isso em condição baixa, feito sujeito à lei; em sofrer as misérias desta vida, a ira de Deus e amaldiçoada morte na cruz; em ser sepultado, e permanecer debaixo do poder da morte durante certo tempo.\n\nRef. Lc 2.7; Fp 2.6-8; Gl 4.4; 3.13; Is 53.3; Mt 27.43; 1Co 15.3-4.",
    28: "PERGUNTA 28. Em que consiste a exaltação de Cristo?\n\nR. A exaltação de Cristo consiste em Ele ressurgir dos mortos no terceiro dia; em subir ao Céu e estar sentado à mão direita de Deus Pai, e em vir para julgar o mundo no último dia.\n\nRef. 1Co 15.4; Ef 1.20-21; At 17.31.",
    29: "PERGUNTA 29. Como nos tornamos participantes da redenção adquirida por Cristo?\n\nR. Tornamo-nos participantes da redenção adquirida por Cristo pela eficaz aplicação dela a nós pelo Seu Santo Espírito.\n\nRef. Jo 1.12; 3.5-6; Tt 3.5-6.",
    30: "PERGUNTA 30. Como nos aplica o Espírito a redenção adquirida por Cristo?\n\nR. O Espírito aplica-nos a redenção adquirida por Cristo, operando em nós a fé, e unindo-nos a Cristo por meio dela em nossa vocação eficaz.\n\nRef. Gl 2.20; Ef 2.8; 1Co 12.12-13.",
    31: "PERGUNTA 31. Que é vocação eficaz?\n\nR. Vocação eficaz é a obra do Espírito Santo, pela qual, convencendo-nos do nosso pecado, e da nossa miséria, iluminando nossos entendimentos pelo conhecimento de Cristo, e renovando a nossa vontade, nos persuade e habilita a abraçar Jesus Cristo, que nos é oferecido de graça no Evangelho.\n\nRef. 1Ts 2.13; At 2.37; 26.18; Ez 36.25-27; 2Tm 1.9; Fp 2.13; Jo 6.37, 44-45.",
    32: "PERGUNTA 32. Que bênçãos gozam nesta vida aqueles que são eficazmente chamados?\n\nR. Aqueles que são eficazmente chamados, gozam, nesta vida, da justificação, adoção e santificação, e das diversas bênçãos que acompanham estas graças ou delas procedem.\n\nRef. Rm 8.30; Ef 1.5; 1Co 1.30.",
    33: "PERGUNTA 33. Que é justificação?\n\nR. Justificação é um ato da livre graça de Deus, no qual Ele perdoa todos os nossos pecados, e nos aceita como justos diante de Si, somente por causa da justiça de Cristo a nós imputada, e recebida só pela fé.\n\nRef. Ef 1.7; 2Co 5.21; Rm 4.6; 5.18; Gl 2.16.",
    34: "PERGUNTA 34. Que é adoção?\n\nR. Adoção é um ato de livre graça de Deus, pelo qual somos recebidos no número dos filhos de Deus, e temos direito a todos os seus privilégios.\n\nRef. 1Jo 3.1; Jo 1.12; Rm 8.14-17.",
    35: "PERGUNTA 35. Que é santificação?\n\nR. É a obra da livre graça de Deus, pela qual somos renovados em todo o nosso ser, segundo a imagem de Deus, e habilitados a morrer cada vez mais para o pecado e a viver para a retidão.\n\nRef. 1Pe 1.2; Ef 4.20-24; Rm 6.6; 12.1-2.",
    36: "PERGUNTA 36. Quais são as bênçãos que nesta vida acompanham a justificação, adoção e santificação ou delas procedem?\n\nR. As bênçãos que nesta vida acompanham a justificação, adoção e santificação, ou delas procedem, são: certeza do amor de Deus, paz de consciência, gozo no Espírito Santo, aumento de graça, e perseverança nela até ao fim.\n\nRef. Rm 5.1-5; 14.17; Jo 1.16; Fp 1.6; 1Pe 1.5.",
    37: "PERGUNTA 37. Quais são as bênçãos que os fiéis recebem de Cristo na hora da morte?\n\nR. As almas dos fiéis na hora da morte são aperfeiçoadas em santidade, e imediatamente entram na glória; e os corpos que continuam unidos Cristo, descansam na sepultura até a ressurreição.\n\nRef. Ap 14.13; Lc 23.43; At 7.55, 59; Fp 1.23; 1Ts 4.14; Jo 5.28-29; 14.2-3; Hb 12.22-23.",
    38: "PERGUNTA 38. Quais são as bênçãos que os fieis recebem de Cristo na ressurreição?\n\nR. Na ressurreição, os fieis, sendo ressuscitados em glória, serão publicamente reconhecidos e absolvidos no dia de juízo, e tornados perfeitamente felizes no pleno gozo de Deus por toda a eternidade.\n\nRef. 1Co 15.43; Mt 10.32; 25.34; Sl 16.11.",
    39: "PERGUNTA 39. Qual é o dever que Deus exige do homem?\n\nR. O dever que Deus exige do homem é obediência à sua vontade revelada.\n\nRef. Mq 6.8; Lc 10.27-28; Gn 17.1.",
    40: "PERGUNTA 40. Que revelou Deus primeiramente ao homem para regra de sua obediência?\n\nR. A regra que Deus revelou primeiramente ao homem para sua obediência foi a lei moral.\n\nRef. Rm 2.14-15.",
    41: "PERGUNTA 41. Onde está a lei moral resumidamente compreendida?\n\nR. A lei moral está resumidamente compreendida nos dez mandamentos.\n\nRef. Dt 10.4; Mt 19.17-19.",
    42: "PERGUNTA 42. Em que se resumem os dez mandamentos?\n\nR. Os dez mandamentos se resumem em amar ao Senhor nosso Deus de todo o nosso coração, de toda a nossa alma, de todas as nossas forças e de todo o nosso entendimento; e ao nosso próximo como a nós mesmos.\n\nRef. Mt 22-37-40.",
    43: "PERGUNTA 43. Qual é o prefácio dos dez mandamentos?\n\nR. O prefácio dos dez mandamentos é: \"Eu sou o Senhor teu Deus, que te tirei da terra do Egito, da casa da servidão\".\n\nRef. Ex 20.2.",
    44: "PERGUNTA 44. Que nos ensina o prefácio dos dez mandamentos?\n\nR. O prefácio dos dez mandamentos ensina-nos que nós temos obrigação de guardar todos os mandamentos de Deus, por ser Ele o Senhor nosso Deus e Redentor.\n\nRef. Dt 11.1; 1Pe 1.15-19.",
    45: "PERGUNTA 45. Qual é o primeiro mandamento?\n\nR. O primeiro mandamento é: \"Não terás outros deuses além de mim\".\n\nRef. Ex 20.3.",
    46: "PERGUNTA 46. Que exige o primeiro mandamento?\n\nR. O primeiro mandamento exige de nós o conhecer e reconhecer a Deus como o único Deus verdadeiro, e nosso Deus; e como tal adorá-lo.\n\nRef. 1Cr 28.9; Dt 26.17; Sl 95.6-7.",
    47: "PERGUNTA 47. Que proíbe o primeiro mandamento?\n\nR. O primeiro mandamento proíbe o negar, ou deixar de adorar ou glorificar ao verdadeiro Deus, como Deus, e nosso Deus; e dar a qualquer outro a adoração e a glória que só a Ele são devidas.\n\nRef. Sl 14.1; Rm 1.20-21, 25; Sl 8.11.",
    48: "PERGUNTA 48. Que se nos ensina especialmente pelas palavras \"além de mim\", no primeiro mandamento?\n\nR. As palavras \"além de mim\", no primeiro mandamento, ensinam-nos que Deus, que vê todas as coisas, toma conhecimento e muito se ofende do pecado de ter-se em seu lugar outro deus.\n\nRef. Sl 139.1-3; Dt 30.17-18.",
    49: "PERGUNTA 49. Qual é o segundo mandamento?\n\nR. O segundo mandamento é: \"Não farás para ti imagem de escultura, nem figura alguma de tudo que há em cima no Céu, e do que há embaixo na terra, nem de coisa alguma que haja nas águas, debaixo da terra. Não as adorarás, nem lhes darás culto; porque eu sou o Senhor teu Deus, o Deus zeloso, que vinga a iniqüidade dos pais nos filhos até à terceira e quarta geração daqueles que me aborrecem; e que usa de misericórdia com milhares daqueles que me amam e que guardam os meus preceitos\".\n\nRef. Ex 20.4-6.",
    50: "PERGUNTA 50. Que exige o segundo mandamento?\n\nR. O segundo mandamento exige que recebamos, observemos e guardemos puros e inteiros todo o culto e ordenanças religiosas que Deus instituiu na sua Palavra.\n\nRef. Dt 12.32; Mt 28.20; Jo 4.23-24.",
    51: "PERGUNTA 51. Que proíbe o segundo mandamento?\n\nR. O segundo mandamento proíbe o adorar a Deus por meio de imagens, ou de qualquer outra maneira não prescrita na sua Palavra.\n\nRef. Rm 1.22-23; 2Rs 18.3-4.",
    52: "PERGUNTA 52. Quais são as razões anexas ao segundo mandamento?\n\nR. As razões anexas ao segundo mandamento são a soberania de Deus sobre nós, a sua propriedade em nós em nós, e o zelo que Ele tem pelo seu culto.\n\nRef. Sl 45.11; 100.3; Ex 34.14; 1Co 10.22.",
    53: "PERGUNTA 53. Qual é o terceiro mandamento?\n\nR. O terceiro mandamento é: \"Não tomarás o nome do Senhor teu Deus em vão, porque o Senhor não terá por inocente aquele que tomar em vão o nome do Senhor seu Deus\".\n\nRef. Ex 20.7.",
    54: "PERGUNTA 54. Que exige o terceiro mandamento?\n\nR. O terceiro mandamento exige o santo e reverente uso dos nomes, títulos, atributos, ordenanças, palavras e obras de Deus.\n\nRef. Sl 29,2; Ap 15.3-4; Ec 5.1; Sl 138.2; 104.24.",
    55: "PERGUNTA 55. O que proíbe o terceiro mandamento?\n\nR. O terceiro mandamento proíbe toda a profanação ou abuso das coisas por meio das quais Deus se faz conhecer.\n\nRef. Lv 19.12; Mt 5.34-35.",
    56: "PERGUNTA 56. Qual é a razão anexa ao terceiro mandamento?\n\nR. A razão anexa ao terceiro mandamento é que, embora os transgressores deste mandamento escapem do castigo dos homens, o Senhor nosso Deus não os deixará escapar do seu justo juízo.\n\nRef. Dt 28.58-59.",
    57: "PERGUNTA 57. Qual é o quarto mandamento?\n\nR. O quarto mandamento é: \"Lembra-te de santificar o dia do Sábado. Trabalharás seis dias, e farás nele tudo o que tens para fazer. O sétimo dia, porém, é o Sábado do Senhor teu Deus. Não farás nesse dia, obra alguma, nem tu, nem teu filho, nem tua filha, nem o teu servo, nem a tua serva, nem o teu animal, nem o peregrino que vive das tuas portas para dentro. Porque o Senhor fez em seis dias o céu, a terra e o mar, e tudo o que neles há, e descansou no sétimo dia. Por isso o Senhor abençoou o dia sétimo e o santificou\".\n\nRef. Ex 20. 8.11.",
    58: "PERGUNTA 58. Que exige o quarto mandamento?\n\nR. O quarto mandamento exige que consagremos a Deus os tempos determinados em sua Palavra, particularmente um dia inteiro em cada sete, para ser um dia de santo descanso a Ele dedicado.\n\nRef. Lv 19.30; Dt 5.12.",
    59: "PERGUNTA 59. Qual dos sete dias designou Deus para esse descanso semanal?\n\nR. Desde o princípio do mundo até à ressurreição de Cristo, Deus designou o sétimo dia da semana para o descanso semanal; e desde então o primeiro dia da semana para continuar sempre até ao fim do mundo, que é o Sábado cristão, ou Domingo.\n\nRef. Gn 2.3; Ex 16.23; At 20.7; 1Co 16.1-2; Ap 1.10.",
    60: "PERGUNTA 60. De que modo se deve santificar o Domingo?\n\nR. Deve-se santificar o Domingo com um santo repouso por todo aquele dia, mesmo das ocupações e recreações temporais que são permitidas nos outros dias; empregando todo o tempo em exercícios públicos e particulares de adoração a Deus, Exceto o tempo preciso para as obras de pura necessidade e misericórdia.\n\nRef. Lv 23.3; Is 58.13-14; Mt 12.11-12; Mc 2.27-28.",
    61: "PERGUNTA 61. Que proíbe o quarto mandamento?\n\nR. O quarto mandamento proíbe a omissão ou a negligência no cumprimento dos deveres exigidos, e a profanação deste dia por meio de ociosidade ou por fazer aquilo que é em si mesmo pecaminoso, ou por desnecessários pensamentos, palavras, ou obras acerca de nossos negócios e recreações temporais.\n\nRef. Jr 17.21; Lc 23.56.",
    62: "PERGUNTA 62. Quais são as razões anexas ao quarto mandamento?\n\nR. As razões anexas ao quarto mandamento são: a permissão que Deus nos concede de fazermos uso dos seis dias da semana para os nossos interesses temporais; o reclamar ele para si a propriedade especial do dia sétimo, o seu próprio exemplo, e a benção que ele conferiu ao dia do descanso.\n\nRef. Ex 31. 15-16; Lv 23.3; Ex 31.17; Gn 2.3.",
    63: "PERGUNTA 63. Qual é o quinto mandamento?\n\nR. O quinto mandamento é: \"Honrarás a teu pai e a tua mãe, para teres uma dilatada vida sobre a terra que o Senhor teu Deus te há de dar\".\n\nRef. Ex 20.12.",
    64: "PERGUNTA 64. Que exige o quinto mandamento?\n\nR. O quinto mandamento exige a conservação da honra e o desempenho dos deveres pertencentes a cada um em suas diferentes condições e relações, como superiores, inferiores, ou iguais.\n\nRef. Ef 6.1-3; Rm 13.1-2; 12.10.",
    65: "PERGUNTA 65. Que proíbe o quinto mandamento?\n\nR. O quinto mandamento proíbe negligenciarmos ou fazermos alguma coisa contra a honra e dever que pertencem a cada um em suas diferentes condições e relações.\n\nRef. Rm 13.7-8.",
    66: "PERGUNTA 66. Qual é a razão anexa ao quinto mandamento?\n\nR. A razão anexa ao quinto mandamento é uma promessa de longa vida e prosperidade (quanto sirva para glória de Deus e bem do homem) a todos aqueles que guardam este mandamento.\n\nRef. Ef 6.2-3.",
    67: "PERGUNTA 67. Qual é o sexto mandamento?\n\nR. O sexto mandamento é: \"Não matarás\".\n\nRef. Ex 20.13.",
    68: "PERGUNTA 68. Que exige o sexto mandamento?\n\nR. O sexto mandamento exige todos os esforços lícitos para conservar a nossa vida e a dos nossos semelhantes.\n\nRef. Sl 132.3-4; At 27.33-34; Rm 12.20-21; Lc 10.33-37.",
    69: "PERGUNTA 69. Que proíbe o sexto mandamento?\n\nR. O sexto mandamento proíbe o tirar a nossa própria vida, ou a do nosso próximo injustamente, e tudo aquilo que para isso concorre.\n\nRef. At 16.28; Gn 9.6; Dt 24.6; Pv 24.11-12; 1Jo 3.15.",
    70: "PERGUNTA 70. Qual é o sétimo mandamento?\n\nR. O sétimo mandamento é: \"Não adulterarás\"\n\nRef. Ex 24.14.",
    71: "PERGUNTA 71. Que exige o sétimo mandamento?\n\nR. O sétimo mandamento exige a conservação da nossa própria castidade, e da do nosso próximo, no coração, nas palavras e nos costumes.\n\nRef. 1Ts 4.4; Ef 4.29; 5.11-12; 1Pe 3.2.",
    72: "PERGUNTA 72. Que proíbe o sétimo mandamento?\n\nR. O sétimo mandamento proíbe todos os pensamentos, palavras e ações impuras.\n\nRef. Mt 5.28; Ef 5.3-4.",
    73: "PERGUNTA 73. Qual é o oitavo mandamento?\n\nR. O oitavo mandamento é: \"Não furtarás\".\n\nRef. Ex 20.15.",
    74: "PERGUNTA 74. Que exige o oitavo mandamento?\n\nR. O oitavo mandamento exige que procuremos o lícito adiantamento das riquezas e do estado exterior, tanto nosso como do nosso próximo.\n\nRef. Pv. 27.23; 22.1-14; Fl 2.4; Ex 23.4-6.",
    75: "PERGUNTA 75. Que proíbe o oitavo mandamento?\n\nR. O oitavo mandamento proíbe tudo o que impede ou pode impedir injustamente o adiantamento da riqueza ou do bem-estar, tanto nosso como do nosso próximo.\n\nRef. Pv 28.19; 1Tm 5.8; Tg 5.1-4.",
    76: "PERGUNTA 76. Qual é o nono mandamento?\n\nR. O nono mandamento é: \"Não dirás falso testemunho contra o teu próximo\".\n\nRef. Ex 20.16.",
    77: "PERGUNTA 77. Que exige o nono mandamento?\n\nR. O nono mandamento exige a conservação e promoção da verdade entre os homens, e a manutenção da nossa boa reputação, e a do nosso próximo, especialmente quando somos chamados a dar testemunho.\n\nRef. Ef 4.25; 1Pe 3.16; At 25.10; 3Jo 12; Pv 14.5, 25; Mt 5.37.",
    78: "PERGUNTA 78. Que proíbe o nono mandamento?\n\nR. O nono mandamento proíbe tudo o que é prejudicial à verdade, ou injurioso, tanto à nossa reputação como à do nosso próximo.\n\nRef. Cl 3.9; 2Co 8.20-21; Sl 15.3; 12.3.",
    79: "PERGUNTA 79. Qual é o décimo mandamento?\n\nR. O décimo mandamento é : \"Não cobiçarás a casa do teu próximo; não desejarás a sua mulher, nem o seu servo, nem a sua serva, nem o seu boi, nem o seu jumento, nem coisa alguma que lhe pertença.\n\nRef. Ex 20.17.",
    80: "PERGUNTA 80. Que exige o décimo mandamento?\n\nR. O décimo mandamento exige o pleno contentamento com a nossa condição, bem como disposição caridosa para com o nosso próximo e tudo o que lhe pertence.\n\nRef. Hb 13.5; 1Tm 6.6-10; Lv 19.18; 1Co 13.4-6.",
    81: "PERGUNTA 81. O que proíbe o décimo mandamento?\n\nR. O décimo mandamento proíbe todo o descontentamento com a nossa condição, todo o movimento de inveja ou pesar à vista da prosperidade do nosso próximo e todas as tendências ou afeições desordenadas a alguma coisa que lhe pertence.\n\nRef. 1Co 10.10; Gl 5.26; Cl 3.5; 1Tm 6.6-10.",
    82: "PERGUNTA 82. Será alguém capaz de guardar perfeitamente os mandamentos de Deus?\n\nR. Nenhum mero homem, desde a queda de Adão, é capaz, nesta vida, de guardar perfeitamente os mandamentos de Deus, mas diariamente os quebranta por pensamentos, palavras e obras.\n\nRef. Rm 3.9-10; Tg 3.2.",
    83: "PERGUNTA 83. São igualmente odiosas todas as transgressões da lei?\n\nR. Alguns pecados em si mesmos, e em razão de circunstâncias agravantes, são mais odiosos à vista de Deus do que outros.\n\nRef. Sl 19.13; Mt 11.24; Lc 12.10; Hb 2.2-3.",
    84: "PERGUNTA 84. Que merece cada pecado?\n\nR. Cada pecado merece a ira e a maldição de Deus, tanto nesta vida como na vindoura.\n\nRef. Gl 3.10; Tg 2.10; Mt 25.41.",
    85: "PERGUNTA 85. Que exige Deus de nós para que possamos escapar a sua ira e maldição em que temos incorrido pelo pecado?\n\nR. Para escaparmos à ira e maldição de Deus, em que temos incorrido pelo pecado, Deus exige de nós fé em Jesus Cristo e arrependimento para a vida, com o uso diligente de todos os meios exteriores pelos quais Cristo nos comunica as bênçãos da redenção.\n\nRef. At 20.21; 2Pe 1.10; Hb 2.3; 1Tm 4.16.",
    86: "PERGUNTA 86. Que é fé em Jesus Cristo?\n\nR. Fé em Jesus Cristo é uma graça salvadora, pela qual o recebemos e confiamos só nEle para a salvação, como Ele nos é oferecido.\n\nRef. At 16.31; Hb 10.39; Jo 1.12; Fp 3.9; Ap 22.17.",
    87: "PERGUNTA 87. Que é arrependimento para a vida?\n\nR. Arrependimento para a vida é uma graça salvadora pela qual o pecador, tendo um verdadeiro sentimento do seu pecado e percepção da misericórdia de Deus em Cristo, se enche de tristeza e de horror pelos seus pecados, abandona-os e volta para Deus, inteiramente resolvido a prestar-lhe nova obediência.\n\nRef. 2Co 7.10; At 2.37; Lc 1.77-79; Jr 31.18-19; Rm 6.18.",
    88: "PERGUNTA 88. Quais são os meios exteriores e ordinários pelos quais Cristo nos comunica as bênçãos da redenção?\n\nR. Os meios exteriores e ordinários pelos quais Cristo nos comunica as bênçãos da redenção, são as suas ordenanças, especialmente a Palavra, os sacramentos e a oração; as quais todas se tornam eficazes aos eleitos para a salvação.\n\nRef. At 2.41-42.",
    89: "PERGUNTA 89. Como se torna a Palavra eficaz para a salvação?\n\nR. O Espírito de Deus torna a leitura e especialmente a pregação da Palavra, meios eficazes para convencer e converter os pecadores, para os edificar em santidade e conforto, por meio da fé para a salvação.\n\nRef. Ne 8.8; At 20.32; Rm 15.4; 2Tm 3.15;.",
    90: "PERGUNTA 90. Como se deve ler e ouvir a Palavra a fim de que ela se torne eficaz para a salvação?\n\nR. Para que a Palavra se torne eficaz para a salvação, devemos ouvi-la com diligência, preparação e oração; recebê-la com fé e amor, guardá-la em nossos corações e praticá-la em nossas vidas.\n\nRef. Dt 6.6-7; 1Pe 2.1-2; Sl 119.11-18; Rm 1.16; 2Ts 2.10; Tg 1.21-25.",
    91: "PERGUNTA 91. Como se tornam os sacramentos meios eficazes para a salvação?\n\nR. Os sacramentos tornam-se meios eficazes para a salvação, não por alguma virtude que eles ou aqueles que os ministram tenham, mas somente pela bênção de Cristo e pela obra do seu Espírito naqueles que pela fé os recebem.\n\nRef. 1Pe 3.21; Rm 2.28-29; 1Co 12.13; 10.16-17.",
    92: "PERGUNTA 92. Que é um sacramento?\n\nR. Um sacramento é uma santa ordenança, instituída por Cristo, na qual, por sinais sensíveis, Cristo e as bênçãos do novo pacto são representadas, seladas e aplicadas aos crentes.\n\nRef. Mt 26.26-28; 28.19; Rm 4.11.",
    93: "PERGUNTA 93. Quais são os sacramentos do Novo Testamento?\n\nR. Os sacramentos do Novo Testamento são o Batismo e a Ceia do Senhor.\n\nRef. At 10.47-48; 1Co 11.23-26.",
    94: "PERGUNTA 94. Que é o Batismo?\n\nR. O Batismo é o sacramento no qual o lavar com água em nome do Pai, do Filho e do Espírito Santo significa e sela a nossa união com Cristo, a participação das bênçãos do pacto da graça, e a promessa de pertencermos ao Senhor.\n\nRef. Mt 28.19; Jo 3.5; Rm 6.1-11; Gl 3.27.",
    95: "PERGUNTA 95. A quem deve ser ministrado o Batismo?\n\nR. O Batismo não deve ser ministrado àqueles que estão fora da igreja visível, enquanto não professarem sua fé em Cristo e obediência a Ele; mas os filhos daqueles que são membros da igreja visível devem ser batizados.\n\nRef. At 18.8; Gn 17.7-14; At 2.38-39; 1Co 7.14.",
    96: "PERGUNTA 96. O que é a Ceia do Senhor?\n\nR. A Ceia do Senhor é o sacramento no qual, dando-se e recebendo-se pão e vinho, conforme a instituição de Cristo, se anuncia a sua morte, e aqueles que participam dignamente tornam-se, não de uma maneira corporal e carnal, mas pela fé, participantes do seu corpo e do seu sangue, com todas as suas bênçãos para o seu alimento espiritual e crescimento em graça.\n\nRef. 1Co 11.23-26; At 3.21; 1Co 10.16.",
    97: "PERGUNTA 97. Que se exige para participar dignamente da Ceia do Senhor?\n\nR. Exige-se daqueles que desejam participar dignamente da Ceia do Senhor que se examine sobre o seu conhecimento em discernir o corpo do Senhor, sobre a sua fé para se alimentarem dele, sobre o seu arrependimento, amor e nova obediência; para não suceder que, vindo indignamente, comam e bebam para si a condenação.\n\nRef. 1Co 11.27; 31-32; Rm 6.17-18.",
    98: "PERGUNTA 98. O que é Oração?\n\nR. A Oração é um santo oferecimento dos nossos desejos a Deus, por coisas conformes com a sua vontade, em nome de Cristo, com a confissão dos nossos pecados, e um agradecido reconhecimento das suas misericórdias.\n\nRef. Sl 10.17; 145.19; 1Jo 5.14; 1.9; Jo 16.23-24; Fp 4.6.",
    99: "PERGUNTA 99. Qual é a regra que Deus nos deu para nos dirigir em oração?\n\nR. Toda palavra de Deus é útil para nos dirigir em oração, mas a regra especial de direção é aquela forma de oração que Cristo ensinou aos seus discípulos, e que geralmente se chama a Oração Dominical.\n\nRef. Rm 8.26; Sl 119.170; Mt 6.9-13.",
    100: "PERGUNTA 100. Que nos ensina o prefácio da Oração Dominical?\n\nR. O prefácio da Oração Dominical, que é: \"Pai nosso que estás no Céu\", ensina-nos que nos devemos aproximar de Deus com toda a santa reverência e confiança, como filhos a um pai poderoso e pronto para nos ajudar, e também nos ensina a orar com os outros e por eles.\n\nRef. Lc 11.13; Rm 8.15; 1Tm 2.1-2.",
    101: "PERGUNTA 101. Pelo que oramos na primeira petição?\n\nR. Na primeira petição que é: \"Santificado seja o Teu nome\" pedimos que Deus nos habilite a nós e aos outros a glorificá-lo em tudo aquilo em que se dá a conhecer; e que disponha tudo para sua glória.\n\nRef. Sl 67.1-3; Rm 11.36; Ap 4.11.",
    102: "PERGUNTA 102. Pelo que oramos na segunda petição?\n\nR. Na segunda petição, que é: \"Venha o Teu reino\", pedimos que o reino de Satanás seja destruído e que o reino da graça seja adiantado; que nós e os outros a ele sejamos guiados e nele guardados, e que cedo venha o reino da glória.\n\nRef. Sl 68.1; Jo 12.31; Mt 9.37-38; 2Ts 3.1; Rm 10.1; Ap 22.20.",
    103: "PERGUNTA 103. Pelo que oramos na terceira petição?\n\nR. Na terceira petição, que é: \"Seja feita Tua vontade, assim na terra como no Céu\", pedimos que Deus, pela sua graça, nos torne capazes e desejosos de conhecer a sua vontade, de obedecer e submeter-nos a ela em tudo, como fazem os anjos no Céu.\n\nRef. Mt 24.39; Fp 1.9-11; Sl 103.20-21.",
    104: "PERGUNTA 104. Pelo que oramos na quarta petição?\n\nR. Na quarta petição, que é: \"O pão nosso de cada dia nos dá hoje\", pedimos que da livre dádiva de Deus recebamos uma porção suficiente das coisas boas desta vida, e gozemos com elas de suas bênçãos.\n\nRef. Pv 30.8-9; 1Tm 6.6-8; Pv 10.22.",
    105: "PERGUNTA 105. Pelo que oramos na quinta petição?\n\nR. Na quinta petição, que é: \"E perdoa-nos as nossas dividas, assim como nós também perdoamos aos nossos devedores\", pedimos que Deus, por amor de Cristo, nos perdoe gratuitamente os nossos pecados, o que somos animados a pedir, porque, pela Sua graça somos habilitados a perdoar de coração ao nosso próximo.\n\nRef. Sl 51.1-2, 7; Mt 18.35.",
    106: "PERGUNTA 106. Pelo que oramos na sexta petição?\n\nR. Na sexta petição, que é: \"E não nos deixes cair em tentação\", pedimos que Deus nos guarde de sermos tentados a pecar, ou nos preserve e livre, quando formos tentados.\n\nRef. Mt 26.41; Sl 19.13; Jo 17.15; 1Co 10.13.",
    107: "PERGUNTA 107. Que nos ensina a conclusão da Oração Dominical?\n\nR. A conclusão da Oração Dominical, que é: \"Porque Teu é o reino, o poder e a glória, para sempre. Amém\", ensina-nos que na Oração devemos confiar somente em Deus, e louvá-lO em nossas orações, atribuindo-Lhe reino, poder e glória. E em testemunho do nosso desejo e certeza de sermos ouvidos, dizemos: Amém.\n\nRef. Dn 9.18-19; Fp 4.6; 1Cr 29.11-13; 1Co 14.16;",
}

jogo_salas_dicas = {
    'inicio':[
        {'cuidado':'entrar com cuidado','tocha':'procurar uma tocha','correndo':'entrar correndo'},
        "Você está na entrada de uma caverna, e está aqui porque foi contratado hoje à tarde para resgatar um cachorro que entrou na caverna e não voltou ainda. \n\nO nome do cachorro é Totó. \n\nDizem que nessa caverna mora um monstro terrível, e também há boatos de que há um tesouro escondido na caverna. Está escuro. Você ouve barulhos estranhos na floresta ao seu redor.\n\n O que você faz?"
        ],
    'dentro_escuro':[
        {'tatear':'tatear no escuro','frente':'ir em frente','fora':'voltar lá pra fora'},
        "Você está dentro da caverna. Aqui há cheiros e ruídos que causam calafrios, e você não consegue enxergar nem um palmo à sua frente. Você ainda consegue enxergar a entrada da caverna, atrás de você. Parece perigoso, mas você será bem pago se resgatar o Totó. O que você quer fazer?"
        ],
    'dentro_escuro_tateando':[
        {'entrada':'voltar para a entrada','continuar':'continuar assim mesmo'},
        "Você resolve tatear ao seu redor, rapidamente tropeça em uma pedra e começa a tatear o chão. Seus dedos tocam algo que parece ser uma moeda, mas você não consegue encontrar o objeto de novo. À sua esquerda e à sua direita, ao tatear o chão, você toca alguma coisa molhada e pegajosa. O líquido da esquerda parece ser mais viscoso e tem um cheiro pior, o da direita lembra um pouco sangue. \n\nO que você vai fazer?"
        ],
    'dentro_escuro_frente':[
        {},
        "Você resolve seguir em frente, mesmo no escuro. Após alguns passos você cai em uma espécie de fosso, e sente seus ossos quebrando no fim da queda. Não foi uma escolha muito boa. Não tem ninguém pra te ajudar. Você não vai ver a luz do dia novamente."
        ],
    'tocha':[
        {'sangue':'seguir o rastro de sangue','moedas':'ir até as moedas','verde':'investigar a gosma verde'},
        "Você procura ao seu redor e encontra perto de um arbusto uma tocha em excelentes condições. Batendo sua espada em uma pedra, você faz uma faísca e acende a tocha. Agora você consegue enxergar dentro da caverna. No interior da caverna você consegue ver uma espécie de fosso muito íngreme alguns metros à sua frente (ainda bem que você pegou uma tocha!). \n\nHá um rastro de sangue à sua esquerda e um rastro de alguma substância gosmenta verde à sua direita. À frente do fosso íngreme você enxerga, no chão, o reflexo de alguma coisa metálica, parecem moedas. \n\nO que você vai fazer?"],
    'dentro':[
        {'sangue':'seguir o rastro de sangue','moedas':'ir até as moedas','verde':'investigar a gosma verde'},
        "Você consegue ver uma espécie de fosso muito íngreme alguns metros à sua frente. \n\nHá um rastro de sangue à sua esquerda e um rastro de alguma substância gosmenta verde à sua direita. À frente do fosso íngreme você enxerga, no chão, o reflexo de alguma coisa metálica, parecem moedas. \n\nO que você vai fazer?"],
    'sangue':[
        {'salvar':'salvar o totó','tesouro':'voltar e procurar o tesouro'},
        "Você segue o rastro de sangue por alguns metros e chega a um salão espaçoso e cheio de pilhas de ossos. Em um canto, no fim do rastro de sangue, está Totó. Ele está olhando para você e abanando o rabo. Uma das patas dele está visivelmente quebrada.\n\n Talvez você consiga levá-lo para fora agora mesmo, encerrando sua missão. Talvez você possa voltar e procurar o tesouro.\n\n O que você vai fazer?"],
    'salvar':[
        {},
        "Você cuidadosamente pega Totó nos braços e segue o caminho de volta para a entrada da caverna. Ele está ferido, mas está feliz de ser resgatado. O que será que o feriu? O que será que era aquele brilho no chão? E aquela gosma verde? Por que será que ele não tentou sair sozinho? Essas perguntas estão no seu coração enquanto você caminha para fora.\n\n Ao se aproximar da entrada, você ouve um barulho muito estranho na direção do rastro de gosma verde, e apressa o passo. Felizmente você consegue sair da caverna e correr pela floresta até a vila. Quando chegar à vila, você será muito bem-recebido e recolherá sua devida recompensa. \n\nParabéns!"],
    'moedas':[
        {'mochila':'guardar o tesouro na mochila','procurar':'voltar e procurar o Totó'},
        "Você  passa pelo fosso e chega a um pequeno salão dentro da caverna. Há moedas espalhadas no chão e um baú aberto, cheio de moedas de ouro e pedras preciosas. Totó não está aqui. O que você vai fazer?"],
    'tesouro':[
        {},
        "Você se ajoelha ao lado do baú e começa a colocar as moedas em sua mochila. O ruído do ouro alegra seu coração, e seu brilho à luz da tocha te anima e faz com que você se imagine realizando todos os seus sonhos. \n\nEnquanto isso, sua imaginação e o barulhinho das pedras preciosas batendo no ouro em sua mochila (enquanto você está enchendo a mochila) te impedem de perceber que alguma criatura enorme e horrenda te seguiu. \n\n Alguma coisa que parece um tentáculo agarra você pelo tronco e outros membros monstruosos que você não consegue identificar direito quebram seus dois braços e suas duas pernas. Enquanto sente a dor terrível, você vê que o ouro está sendo derramado da sua mochila de volta para o baú, e em seguida você é arrastado até uma outra sala. Nessa outra sala, cheia de ossos, está Totó, com uma patinha quebrada, tremendo de medo num canto. Após deixar você no canto oposto deste salão, o monstro se retira, deixando a tocha. Você não está no escuro, mas preferia não enxergar o que vai acontecer a seguir. Não vamos entrar em detalhes.\n\n Você fez a escolha errada."],
    'gosma':[
        {'surpresa':'ataque surpresa','cuidadosamente':'voltar cuidadosamente','alavanca':'acionar a alavanca','corda':'puxar a corda'},
        "Ao seguir o rastro, você encontra um salão todo cheio de gosma. À sua direita tem uma corda pendurada. Embaixo dela, há uma espécie de alavanca encaixada em algum mecanismo na parede. No centro do salão, de costas para você (ou pelo menos parece estar de costas) está uma criatura horrível, com tentáculos saindo da cabeça, seis membros que parecem ser pernas ou braços, grandes asas como de morcego e coberta de espinhos, como um ouriço. \n\nA criatura parece estar dormindo, mas você não tem certeza. \n\nO que você vai fazer?"],
    'sorte':[
        {},
        "Você ataca o monstro antes dele conseguir atacar você. Com sua espada, você desfere golpes onde parece ser mais macio, mas você não está enxergando direito porque precisou soltar a tocha no chão. O monstro também te ataca com seus braços (ou pernas?) e tentáculos, e logo a seguir você sente que há alguma espécie de ácido agindo sobre a sua pele. \n\nA batalha não dura muito tempo, você consegue encravar sua espada no centro do abdome do monstro e rasgar o que parece ser a barriga dele, até o chão.\n O monstro gorgoleja uns sons que vão ficar nos seus pesadelos por muitos anos ainda e sai andando, cambaleando, fugindo de você! Você vai seguindo e vê que o monstro tropeçou e caiu no fosso! Você ouve ainda os guinchos de agonia lá embaixo, mas o barulho cessa depois de algum tempo. \nVocê continua vasculhando a caverna e encontra um baú cheio de moedas de ouro e pedras preciosas, e enche sua mochila. \nVocê também encontra um salão amplo, cheio dos ossos das vítimas do monstro, e no canto do salão está o Totó. Ele vai na sua direção mancando, está com uma pata quebrada, e provavelmente estava sendo guardado pelo monstro para se transformar em uma refeição mais tarde. Totó te segue para fora da caverna, e vocês vão pela floresta em direção à vila. A noite terrível está terminando. Parabéns!"],
    'azar':[
        {},
        "O monstro te ataca e fere seu braço antes de você conseguir preparar sua espada direito. \n\nVocê consegue se defender de alguns golpes, e até consegue atacar também, mas seu braço parece estar mais fraco que o normal (talvez seja algum tipo de veneno agindo), e os seus golpes todos são superficiais. \n\nApós alguns instantes, o monstro dá um golpe com uma espécie de cauda que você nem tinha visto, e sua cabeça é separada do seu corpo. \n\nVocê chegou perto, mas morreu. \n\nVocê será devorado pelo monstro mais tarde, e amanhã Totó vai servir de lanche."],
    'alavanca':[
        {},
        "Você aciona a alavanca, se questionando se isso é mesmo uma boa ideia. \n\nEsta caverna era o começo de uma mina antes do monstro subir das profundezas e matar todos os envolvidos. \n\nA tal alavanca causa um barulho muitos metros acima do monstro, que se vira, olha pra você e vai deslizando na sua direção. \n\nQuando ele chega bem perto, um carrinho cheio de pedras cai exatamente em cima dele, esmagando-o completamente, lançando seu sangue e suas tripas para todos os lados. Você sente o gosto das tripas do monstro, mas nem fica tão triste com isso. A alavanca aparentemente era conectada a algum mecanismo que estava mantendo o carrinho parado lá em cima, há muitos anos. Com o monstro evidentemente morto, você está livre para vasculhar o resto da caverna. \n\n Em um dos salões você encontra um baú cheio de moedas de ouro e pedras preciosas, e enche sua mochila. \nVocê também encontra um salão amplo, cheio dos ossos das vítimas do monstro, e no canto do salão está o Totó. Ele vai na sua direção mancando, está com uma pata quebrada, e provavelmente estava sendo guardado pelo monstro para se transformar em uma refeição mais tarde. Você o pega nos braços e sai da caverna, indo pela floresta em direção à vila. \n\nParabéns!"
        ],
    'corda':[
        {'atacar':'se defender do monstro que se aproxima'},
        "Você puxa a corda com a esperança de que isso sirva de alguma coisa. \n\nServe: a corda aciona uma espécie de sino, um alarme! \n\nO monstro, ao ouvir o barulho, faz um rápido giro e vai deslizando na sua direção. \n\nParece que você vai ter que lutar."
        ],
    }
jogo_escolha_sala = {
    'cuidado':'dentro_escuro',
    'tocha':'tocha',
    'tatear':'dentro_escuro_tateando',
    'frente':'dentro_escuro_frente',
    'continuar':'dentro_escuro_frente',
    'correndo':'dentro_escuro_frente',
    'fora':'inicio',
    'entrada':'inicio',
    'sangue':'sangue',
    'moedas':'moedas',
    'verde':'gosma',
    'salvar':'salvar',
    'tesouro':'dentro',
    'procurar':'dentro',
    'cuidadosamente':'dentro',
    'mochila':'tesouro',
    'alavanca':'alavanca',
    'corda':'corda',
    'sorte':'sorte',
    'azar':'azar',
    'gameover':'gameover',
    }

triggers_calvinista = [
    "calvinista",
    "maldito",
    "ninjas",
    "crente",
    "cosmovisao",
    "cosmovisão",
    "predestin",
    "eleito",]
triggers_conselho = [
    "conselho",
    "dica",
    "aconselhamento",
    "sugere",]
triggers_computador = [
    "computador",
    "impressora",
    "internet",
    "ajuda",
    "T.I",]
resposta_calvinista = [
    "MALDITOS NINJAS CALVINISTAS!!1! (shhhh...)",
    "'mas-e-ser-veto-hein?'",
    "predestinado a ser NINJA",
    "eleitos, reacionários e discretos...",
    "COSMOVISÃO CRISTÃ? isso sim é perigoso!",
    "T.U.L.I.P. (todos unidos louvando [em uma] igreja presbiteriana)",
    "B.A.C.O.N. (bandidos completos, adotados sem mérito, certeza que só alguns vão pro céu, óbvio que Deus é mais forte, nunca perdidos)",]
resposta_conselho = [
    "Se conselho fosse bom não se dava, se vendia",
    "Conselho bom só se for o da minha igreja (badumtss)",
    "Não estamos trabalhando com aconselhamento automático, obrigado",
    "Leia a bíblia e faça oração se quiser crescer...",
    "... quem não ora e a bíblia não lê, diminuirá!",]
resposta_computador = [
    "Não sei, espero ter ajudado.",
    "Já tentou desligar e ligar de novo?",
    "Já verificou se todos os cabos estão conectados?",
    "Acho que você precisa comprar uma impressora nova.",
    "Deve ser problema de BIOS (bacana inocente operando o sistema)",]
resposta_geral = [
    "Fala aí!",
    "Ô cafezinho bom...",
    "Sim!",
    "Não!?",
    "Eitaaa...",
    "Opa!",
    "Oi?",
    "Eae blz?",
    "Tranquilo?",
    "Na paz?",
    "Sério?",
    "Você já jogou comigo na DM? Vai lá e diz 'quero jogar'",
    "Vai lá na DM e diz 'BCW 1' pra ver o que acontece =]",]

now = datetime.datetime.now()
last_hour = now.hour
last_minute = now.minute

def check_mentions(api, since_id):

    ################################## parte dos follows e unfollows
    global last_hour
    now = datetime.datetime.now()
    if last_hour != now.hour:
        try:
            time.sleep(30)
            logger.info("Já passou uma hora, vamos verificar se mudou algo nos followers e friends")
            last_hour = now.hour
            for follower in tweepy.Cursor(api.followers).items():
                if not follower.following:
                    logger.info(f"Following {follower.name}")
                    follower.follow()
            logger.info("Já verifiquei os followers, agora vou esperar 1 minuto pra verificar os friends")
            time.sleep(60)
            for friend in tweepy.Cursor(api.friends).items():
                if friend not in tweepy.Cursor(api.followers).items():
                    logger.info(f"UN-Following {friend.name}")
                    api.destroy_friendship(friend.id)
        except:
            logger.info("deu problema no follow-unfollow automático.")


    ################################## parte das DM
    logger.info("Vou verificar se tem alguma DM nova (e responder).")
    dmlist = api.list_direct_messages()
    for dm in dmlist:
        if(dm.message_create['target']['recipient_id'] == '1225135484109836289'):#'1225135484109836289' sou eu.
            try:
                ########### verificando se já estava conversando na DM (inicio)
                try:
                    #apesar de ter 'timestamps' no nome da pasta, o que tem lá é o id da DM mesmo.
                    last_dm_read = open('timestamps_dm/last_dm'+str(dm.message_create['sender_id']),'r')
                    last_dm = last_dm_read.read()
                    last_dm_read.close()
                except:
                    last_dm = 0
                    logger.info("deu problema lendo id da ultima dm")
                ########### verificando se já estava conversando na DM (fim)

                if(int(dm.id) > int(last_dm)):
                    ########################## só entra aqui se for DM mais nova do que o que eu tenho anotado (e ele olha só a mais nova)
                    texto = dm.message_create['message_data']['text'].lower().strip()

                    ########### coisas do joguinho (inicio)
                    jogando_linha = ""
                    jogando = False
                    gameover = False
                    try:
                        jogando_read = open('joguinho/jogando'+str(dm.message_create['sender_id']),'r')
                        jogando_linha = jogando_read.read()
                        jogando_read.close()
                        jogando = True
                    except:
                        logger.info("Deu problema preparando joguinho")

                    if jogando_linha == 'gameover':
                        gameover = True
                    if (texto == "quero jogar de novo"):
                        texto = "quero jogar"
                        jogando = False
                        gameover = False
                    if (texto == "quero jogar") and not (jogando or gameover):
                        jogando_write = open('joguinho/jogando'+dm.message_create['sender_id'],'w')
                        jogando_write.write('inicio')
                        jogando_write.close()
                        logger.info(dm.message_create['sender_id'] + " entrou no jogo!")
                        api.send_direct_message(dm.message_create['sender_id'], "Que legal, você quer jogar! Aqui vão algumas regras: \n\n 1 - Eu demoro uns dois a cinco minutos para ler suas respostas. E eu só leio a sua última resposta. Não escreva várias DM, eu só vou ler a última.\n\n 2 - É um jogo de aventura daqueles em que você faz escolhas, então você tem que escrever o que quer fazer a cada cena. \n\n 3 - Eu _sempre_ vou repetir a descrição da cena/sala em que você está (juntamente com as respostas válidas). \n\n 4 - Se quiser conversar com o programador, é o @daniel_ishy, fala lá com ele se perceber algo estranho\n\n 5 - Se quiser encerrar o jogo, diga 'gameover'. \n\n\n\n Vamos começar em alguns segundos!")
                        time.sleep(1)
                        jogando = True
                        gameover = False
                        jogando_linha = 'inicio' #pra nao ter que ler de novo o arquivo...
                        dicas = jogo_salas_dicas[jogando_linha][0]
                        descricao = jogo_salas_dicas[jogando_linha][1]
                    if(jogando and not gameover):
                        if jogando_linha == "":
                            jogando_linha = 'inicio'
                            logger.info('aparentemente a linha chegou vazia aqui, o que não devia acontecer...')
                        dicas = jogo_salas_dicas[jogando_linha][0]
                        comando = texto
                        if(comando == 'gameover'):
                            jogando_write = open('joguinho/jogando'+dm.message_create['sender_id'],'w')
                            jogando_write.write('gameover')
                            jogando_write.close()
                            api.send_direct_message(dm.message_create['sender_id'], "Mas já? Que pena então... \n\nObrigado por jogar!")
                            time.sleep(1)
                        elif(comando in dicas.keys()):
                            if(comando == 'surpresa'):
                                api.send_direct_message(dm.message_create['sender_id'], "Nesta luta, você atacará de surpresa, tendo 80% de chance de vitória! \n\n(aguarde o resultado)")
                                time.sleep(1)
                                resultado = random.choice(['sorte','sorte','sorte','azar','sorte'])
                                jogando_write = open('joguinho/jogando'+dm.message_create['sender_id'],'w')
                                jogando_write.write(resultado)
                                jogando_write.close()
                            elif(comando == 'atacar'):
                                api.send_direct_message(dm.message_create['sender_id'], "Nesta luta, você começará se defendendo, tendo 40% de chance de vitória...\n\n(aguarde o resultado)")
                                time.sleep(1)
                                resultado = random.choice(['sorte','azar','azar','azar','sorte'])
                                jogando_write = open('joguinho/jogando'+dm.message_create['sender_id'],'w')
                                jogando_write.write(resultado)
                                jogando_write.close()
                            else: #comando válido
                                jogando_write = open('joguinho/jogando'+dm.message_create['sender_id'],'w')
                                jogando_write.write(jogo_escolha_sala[comando])
                                jogando_write.close()
                        else:
                            if comando != 'quero jogar': #pra não dar essa mensagem no primeiro momento.
                                api.send_direct_message(dm.message_create['sender_id'], "A mensagem que você enviou por último não é uma das escolhas válidas.\n\n Por favor, tente de novo.")
                                time.sleep(1)

                        try:
                            if(not gameover and jogando_linha != 'gameover'):
                                jogando_read = open('joguinho/jogando'+str(dm.message_create['sender_id']),'r')
                                jogando_linha = jogando_read.read()
                                jogando_read.close()
                                dicas = jogo_salas_dicas[jogando_linha][0]
                                descricao = jogo_salas_dicas[jogando_linha][1]

                                texto_resposta = descricao

                                if(dicas):
                                    texto_resposta = texto_resposta + "\nRespostas válidas:\n - "+'\n - '.join('{} : {}'.format(key, value) for key, value in dicas.items())
                                else:
                                    texto_resposta = texto_resposta + "\n Foi muito legal jogar com você! \nObrigado!\n Ah sim, se quiser jogar de novo diga assim:\n'quero jogar de novo'"
                                    jogando_write = open('joguinho/jogando'+dm.message_create['sender_id'],'w')
                                    jogando_write.write('gameover')
                                    jogando_write.close()
                                    gameover = True
                                api.send_direct_message(dm.message_create['sender_id'],texto_resposta)
                                time.sleep(1)
                        except:
                            logger.info("Deu problema na hora de mostrar mensagem do joguinho")
                            pass

                    ########### coisas do joguinho (fim)

                    else:
                        ##### Entra aqui quando não está jogando.
                        if(texto.find('bcw') == 0):
                            try:
                                pergunta = int(texto.split(' ')[1])
                            except:
                                pergunta = 1
                                logger.info("Deu problema no 'índice' do breve catecismo de westminster")

                            resposta = bcw.get(pergunta, "Hmm, não encontrei a pergunta '"+str(pergunta)+"'.")

                        else:
                            print('nao tem bcw, texto = '+texto)
                            resposta = random.choice(resposta_geral)+"\n\nSua mensagem foi recebida, obrigado! \n\n Já tentou digitar as opções 'bcw 1' ou 'quero jogar'?"

                        api.send_direct_message(dm.message_create['sender_id'], resposta)
                        logger.info("respondi, vou gravar o id (da dm recebida) e esperar 5 segundos.")

                    #sempre executar ao tratar qualquer DM nova:
                    logger.info("Respondi uma DM (de id="+str(dm.id)+") do usuário "+str(dm.message_create['sender_id']))
                    last_dm_write = open('timestamps_dm/last_dm'+dm.message_create['sender_id'],'w')
                    last_dm_write.write(dm.id)
                    last_dm_write.close()
                    time.sleep(1)
            except:
                    logger.info("Deu problema na DM")

    ############################## terminou a parte de DM
    ############################## começou tweets com mentions

    logger.info("em t-3: Recuperando mentions desde a do id "+str(since_id))
    time.sleep(3)
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        try:
            new_since_id = max(tweet.id, int(new_since_id))
            logger.info(f"Respondendo {tweet.user.name}")
            logger.info("tweet.id:"+str(new_since_id))
            if not tweet.favorited:
                try:
                    tweet.favorite()
                except Exception as e:
                    logger.error("Deu problema favoritando", exc_info=True)

            tweettextlower = tweet.text.lower()
            time.sleep(1)
            if any(keyword in tweettextlower for keyword in triggers_calvinista):
                logger.info('keyword calvinista')
                api.update_status(
                    status=random.choice(resposta_calvinista),
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            elif any(keyword in tweettextlower for keyword in triggers_conselho):
                logger.info('keyword conselho')
                api.update_status(
                    status=random.choice(resposta_conselho),
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            elif any(keyword in tweettextlower for keyword in triggers_computador):
                logger.info('keyword computador')
                api.update_status(
                    status=random.choice(resposta_computador),
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            elif any(keyword in tweettextlower for keyword in ["bom dia"]):
                logger.info('bom dia')
                api.update_status(
                    status="bom dia!",
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            elif any(keyword in tweettextlower for keyword in ["boa tarde"]):
                logger.info('boa tarde')
                api.update_status(
                    status="boa tarde!",
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            elif any(keyword in tweettextlower for keyword in ["boa noite"]):
                logger.info('boa noite')
                api.update_status(
                    status="boa noite!",
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            elif any(keyword in tweettextlower for keyword in ["catecismo de westminster"]):
                logger.info('boa noite')
                api.update_status(
                    status="Eu tenho um catecismo na DM, vai lá e diz 'bcw 1'. Peguei lá no site antigo da @monergismo.",
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            else:
                logger.info('sem keyword')
                api.update_status(
                    status=random.choice(resposta_geral),
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
            logger.info("Salvando id do último tweet respondido:"+str(new_since_id)+" ...")
            since_id_write = open('last_id','w')
            since_id_write.write(str(new_since_id))
            since_id_write.close()
        except:
            logger.info("deu problema na twitada.")
    return new_since_id



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


auth = tweepy.OAuthHandler(twitterauth.auth1, twitterauth.auth2)
auth.set_access_token(twitterauth.token1, twitterauth.token2)

api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
try:
    api.verify_credentials()
except Exception as e:
    logger.error("Error creating API", exc_info=True)
    raise e
logger.info("API created")

while True:
    since_id_read = open('last_id','r')
    since_id = since_id_read.read()
    since_id_read.close()

    since_id = str(check_mentions(api, since_id))

    logger.info("Esperando 1 minuto...")
    time.sleep(60)


