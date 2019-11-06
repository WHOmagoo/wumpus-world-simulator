project(wumpus-world)
cmake_minimum_required(VERSION 3.3)

set (CMAKE_CXX_STANDARD 98)

#file(GLOB wumpus-world-headers "*.h")
aux_source_directory(. SRC_LIST)

list (REMOVE_ITEM SRC_LIST ./PyAgent.cc)


add_executable(wumpus-world Action.h Agent.h Orientation.h wumpsim.h WumpusWorld.h ${SRC_LIST})


message(STATUS "files included" ${SRC_LIST})