# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.8

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/debian/ADALM2000/cmake-3.8.2/Bootstrap.cmk/cmake

# The command to remove a file.
RM = /home/debian/ADALM2000/cmake-3.8.2/Bootstrap.cmk/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/debian/ADALM2000/cmake-3.8.2

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/debian/ADALM2000/cmake-3.8.2

# Include any dependencies generated for this target.
include Utilities/cmcompress/CMakeFiles/cmcompress.dir/depend.make

# Include the progress variables for this target.
include Utilities/cmcompress/CMakeFiles/cmcompress.dir/progress.make

# Include the compile flags for this target's objects.
include Utilities/cmcompress/CMakeFiles/cmcompress.dir/flags.make

Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o: Utilities/cmcompress/CMakeFiles/cmcompress.dir/flags.make
Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o: Utilities/cmcompress/cmcompress.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/debian/ADALM2000/cmake-3.8.2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o"
	cd /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress && /usr/bin/gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/cmcompress.dir/cmcompress.c.o   -c /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress/cmcompress.c

Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/cmcompress.dir/cmcompress.c.i"
	cd /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress && /usr/bin/gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress/cmcompress.c > CMakeFiles/cmcompress.dir/cmcompress.c.i

Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/cmcompress.dir/cmcompress.c.s"
	cd /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress && /usr/bin/gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress/cmcompress.c -o CMakeFiles/cmcompress.dir/cmcompress.c.s

Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o.requires:

.PHONY : Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o.requires

Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o.provides: Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o.requires
	$(MAKE) -f Utilities/cmcompress/CMakeFiles/cmcompress.dir/build.make Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o.provides.build
.PHONY : Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o.provides

Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o.provides.build: Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o


# Object files for target cmcompress
cmcompress_OBJECTS = \
"CMakeFiles/cmcompress.dir/cmcompress.c.o"

# External object files for target cmcompress
cmcompress_EXTERNAL_OBJECTS =

Utilities/cmcompress/libcmcompress.a: Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o
Utilities/cmcompress/libcmcompress.a: Utilities/cmcompress/CMakeFiles/cmcompress.dir/build.make
Utilities/cmcompress/libcmcompress.a: Utilities/cmcompress/CMakeFiles/cmcompress.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/debian/ADALM2000/cmake-3.8.2/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C static library libcmcompress.a"
	cd /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress && $(CMAKE_COMMAND) -P CMakeFiles/cmcompress.dir/cmake_clean_target.cmake
	cd /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cmcompress.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
Utilities/cmcompress/CMakeFiles/cmcompress.dir/build: Utilities/cmcompress/libcmcompress.a

.PHONY : Utilities/cmcompress/CMakeFiles/cmcompress.dir/build

Utilities/cmcompress/CMakeFiles/cmcompress.dir/requires: Utilities/cmcompress/CMakeFiles/cmcompress.dir/cmcompress.c.o.requires

.PHONY : Utilities/cmcompress/CMakeFiles/cmcompress.dir/requires

Utilities/cmcompress/CMakeFiles/cmcompress.dir/clean:
	cd /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress && $(CMAKE_COMMAND) -P CMakeFiles/cmcompress.dir/cmake_clean.cmake
.PHONY : Utilities/cmcompress/CMakeFiles/cmcompress.dir/clean

Utilities/cmcompress/CMakeFiles/cmcompress.dir/depend:
	cd /home/debian/ADALM2000/cmake-3.8.2 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/debian/ADALM2000/cmake-3.8.2 /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress /home/debian/ADALM2000/cmake-3.8.2 /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress /home/debian/ADALM2000/cmake-3.8.2/Utilities/cmcompress/CMakeFiles/cmcompress.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : Utilities/cmcompress/CMakeFiles/cmcompress.dir/depend

