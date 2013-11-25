Mini-project description 
========================
Rock-paper-scissors-lizard-Spock
--------------------------------

Rock-paper-scissors is a hand game that is played by two people. The players count to three in unison and simultaneously throw one of three hand signals that correspond to rock, paper or scissors. The winner is determined by the rules:

* Rock smashes scissors
* Scissors cuts paper
* Paper covers rock

Rock-paper-scissors is a surprisingly popular game that many people play seriously (see the [Wikipedia article](http://en.wikipedia.org/wiki/Rock_paper_scissors) for details). Due to the fact that a tie happens around 1/3 of the time, several variants of Rock-Paper-Scissors exist that include more choices to make ties more unlikely.

Rock-paper-scissors-lizard-Spock (RPSLS) is a variant of Rock-paper-scissors that allows five choices. Each choice wins against two other choices, loses against two other choices and ties against itself. Much of RPSLS's popularity is that it has been featured in 3 episodes of the TV series "The Big Bang Theory". The [Wikipedia entry](http://en.wikipedia.org/wiki/Rock-paper-scissors-lizard-Spock) for RPSLS gives the complete description of the details of the game.

In our first mini-project, we will build a Python function <code>"rpsls(name)"</code> that takes as input the string name, which is one of <code>"rock"</code>, <code>"paper"</code>, <code>"scissors"</code>, <code>"lizard"</code>, or <code>"Spock"</code>. The function then simulates playing a round of Rock-paper-scissors-lizard-Spock by generating its own random choice from these alternatives and then determining the winner using a simple rule that we will next describe.

While Rock-paper-scissor-lizard-Spock has a set of ten rules that logically determine who wins a round of RPSLS, coding up these rules would require a large number (5x5=25) of <code>if</code>/<code>elif</code>/<code>else</code> clauses in your mini-project code. A simpler method for determining the winner is to assign each of the five choices a number:

0 — rock  
1 — Spock  
2 — paper  
3 — lizard  
4 — scissors  

In this expanded list, each choice wins against the preceding two choices and loses against the following two choices.
