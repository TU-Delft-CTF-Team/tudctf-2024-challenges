.PHONY: debug

lumberjack: lumberjack.o
	g++ -o lumberjack lumberjack.o

lumberjack.o: lumberjack.cpp
	g++ -Wall -Wextra -Wpedantic -std=c++20 -O0 -c -o lumberjack.o lumberjack.cpp

debug: lumberjack.cpp
	g++ -Wall -Wextra -Wpedantic -std=c++20 -g -o lumberjack lumberjack.cpp