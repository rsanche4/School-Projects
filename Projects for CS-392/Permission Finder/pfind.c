/*******************************************************************************
 * Name        : pfind.c
 * Author      : Sydney Cardy and Rafael Sanchez
 * Date        : 16 March 2021
 * Description : Finds all files in the system with the given perms
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <time.h>
#include <limits.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>

void recurse_through_dirs(char *path, char *permission_string) {
	//After this, all of the arguments that were passed are now in the correct format, SUPPOSEDLY.
	//So what we will do is open the directory specified, then read all the files, and match with permission string. If they match, output it.
	DIR *dir;
	struct dirent *entry;

	//open the directory specified. We assume it's a real directory, because we already checked for that before, but just in case we check.
	dir = opendir(path);

	//then check if we are at the root. If we are, get rid of the extra slash
		if (path[0] == '/' && path[1] == '/') {
			for (int i = 0; i < PATH_MAX-1; i++) {
				path[i] = path[i+1];
			}
		}

	if (dir == NULL) {

			fprintf(stderr, "Error: Cannot open directory '%s'. %s.\n",
							path, strerror(errno));
					return;
		}



	while ((entry = readdir(dir)) != NULL) {
		if ((strcmp(entry->d_name, ".") == 0) ||
				(strcmp(entry->d_name, "..") == 0)) {
			continue;
		} // if it's a dot or a dot dot, just continue

		if (entry->d_type == DT_DIR) {
			char newpath[PATH_MAX]; //TODO WE setill need to check if a folder has permissions to go in, otherwise output we can't access it and continue
			strcpy(newpath, path);
			strcat(newpath, "/"); //concatenate to path the folder AND a back slash
			strcat(newpath, entry->d_name);
			struct stat current_file_permission;
			if (lstat(newpath, &current_file_permission) < 0) {

				fprintf(stderr, "Error: Cannot stat '%s'. %s.\n",
						entry->d_name, strerror(errno));
				continue;
			}
			//if we can stat it though, then ask if it matches the permission string given
			//First create an array with permission strings for this file
			char permissions_of_file[10];
			permissions_of_file[9] = '\0';
			int perms[] = {S_IRUSR, S_IWUSR, S_IXUSR,
					S_IRGRP, S_IWGRP, S_IXGRP,
					S_IROTH, S_IWOTH, S_IXOTH};

			int permission_valid;
			for (int i = 0; i < 9; i+=3) {
				permission_valid = current_file_permission.st_mode & perms[i];
				if (permission_valid) {
					permissions_of_file[i] = 'r';
				} else {
					permissions_of_file[i] = '-';
				}
				permission_valid = current_file_permission.st_mode & perms[i+1];
				if (permission_valid) {
					permissions_of_file[i+1] = 'w';
				}  else {
					permissions_of_file[i+1] = '-';
				}
				permission_valid = current_file_permission.st_mode & perms[i+2];
				if (permission_valid) {
					permissions_of_file[i+2] = 'x';
				}  else {
					permissions_of_file[i+2] = '-';
				}
			}
			if (strcmp(permissions_of_file, permission_string) == 0) {
				printf("%s\n", newpath);
			}

			recurse_through_dirs(newpath, permission_string);
			//put this in a recursive function, and just call it again on this directory
			//and then when you get to a file, match the stats with the stats given and if they are the same output that file.
			//then keep going down the recursion tree

		} else {
			char newpath[PATH_MAX];
			strcpy(newpath, path);
			strcat(newpath, "/"); //concatenate to path the folder AND a back slash
			strcat(newpath, entry->d_name);
			//so now that we have reached a file, we want to check its permission
			struct stat current_file_permission;
			if (lstat(newpath, &current_file_permission) < 0) {
				fprintf(stderr, "Error: Cannot stat '%s'. %s.\n",
						entry->d_name, strerror(errno));
				continue;
			}
			//if we can stat it though, then ask if it matches the permission string given
			//First create an array with permission strings for this file
			//(stat(arg_d, &statbuf) < 0)

			char permissions_of_file[10];
			permissions_of_file[9] = '\0';
			int perms[] = {S_IRUSR, S_IWUSR, S_IXUSR,
					S_IRGRP, S_IWGRP, S_IXGRP,
					S_IROTH, S_IWOTH, S_IXOTH};

			int permission_valid;
			for (int i = 0; i < 9; i+=3) {
				permission_valid = current_file_permission.st_mode & perms[i];
				if (permission_valid) {
					permissions_of_file[i] = 'r';
				} else {
					permissions_of_file[i] = '-';
				}
				permission_valid = current_file_permission.st_mode & perms[i+1];
				if (permission_valid) {
					permissions_of_file[i+1] = 'w';
				}  else {
					permissions_of_file[i+1] = '-';
				}
				permission_valid = current_file_permission.st_mode & perms[i+2];
				if (permission_valid) {
					permissions_of_file[i+2] = 'x';
				}  else {
					permissions_of_file[i+2] = '-';
				}
			}
			if (strcmp(permissions_of_file, permission_string) == 0) {
				//then check if we are at the root. If we are, get rid of the extra slash
						if (newpath[0] == '/' && newpath[1] == '/') {
							for (int i = 0; i < PATH_MAX-1; i++) {
								newpath[i] = newpath[i+1];
							}
						}

				printf("%s\n", newpath);
			}
		}
	}

	closedir(dir);
}

void display_usage() {
	printf("Usage: ./pfind -d <directory> -p <permissions string> [-h]\n");
}

int main (int argc, char *argv[]) {

	if (argc == 1) {
		display_usage();
		return EXIT_FAILURE;
	}

	int c;
	char *directory = NULL;
	char *permission_string = NULL;
	opterr = 0;
	//RIGHT HERE WE NEED TO ADAPT OUR CODE AND LEARN TO USE :d:p:h etc. AFTER THAT WE ARE DONE AND WE CAN START THE RECURSION TREE. USE OPTARG
	int numd = 0;
	int nump = 0;
	while ( (c = getopt (argc, argv, "d:p:h")) != -1 ) {
		switch (c) {
		case 'd':
			directory = optarg;
			numd = 1;
			break;
		case 'p':
			permission_string = optarg;
			nump = 1;
			break;
		case 'h':
			display_usage();
			return EXIT_SUCCESS;
		case '?':
			if (optopt == 'd') {
				printf("Error: Required argument -d <directory> not found.\n");
				return EXIT_FAILURE;
			} else if (optopt == 'p' && numd == 0) {
				printf("Error: Required argument -d <directory> not found.\n");
				return EXIT_FAILURE;
			} else if (optopt == 'p') {
				printf("Error: Required argument -p <permissions string> not found.\n");
				return EXIT_FAILURE;
			} else {
				fprintf (stderr, "Error: Unknown option '-%c' received.\n", optopt);
				return EXIT_FAILURE;
			}
		default:
			abort();
		}
	}
	if (numd + nump != 2) {
		if (numd != 0) {
			printf("Error: Required argument -p <permissions string> not found.\n");
			return EXIT_FAILURE;
		} else if (nump != 0) {
			printf("Error: Required argument -d <directory> not found.\n");
			return EXIT_FAILURE;
		}
	}

	//argv[3] has the first director and permission_string has the permissions. Note right, here this SHOULD CHECK for permission denied thingy.
	struct stat sb;
	if (stat(directory, &sb) < 0) {
		fprintf(stderr, "Error: Cannot stat '%s'. %s.\n",
				directory, strerror(errno));
		return EXIT_FAILURE;
	}

	//At this point we have a good directory or a file. Next is permission strings
	if (strlen(permission_string) != 9) {
		printf("Error: Permissions string '%s' is invalid.\n", permission_string);
		return EXIT_FAILURE;
	} else {
		for (int i = 0; i < 9; i += 3) {
			if (permission_string[i] != 'r' && permission_string[i] != '-') {
				printf("Error: Permissions string '%s' is invalid.\n", permission_string);
				return EXIT_FAILURE;
			}
			if (permission_string[i+1] != 'w' && permission_string[i+1] != '-') {
				printf("Error: Permissions string '%s' is invalid.\n", permission_string);
				return EXIT_FAILURE;
			}
			if (permission_string[i+2] != 'x' && permission_string[i+2] != '-') {
				printf("Error: Permissions string '%s' is invalid.\n", permission_string);
				return EXIT_FAILURE;
			}
		}
	}

	//Supposing everything was good before this, let's try to get the real path of the directory given
	char path[PATH_MAX];
	if (realpath(directory, path) == NULL) {
		fprintf(stderr, "Error: Cannot get full path of file '%s'. %s.\n",
				argv[1], strerror(errno));
		return EXIT_FAILURE;
	}

	//so now we are here, with the real path of the directory, and we assume that we can in fact access this directory
	//if it is a real directory, recurese through it and match with the permissions
	recurse_through_dirs(path, permission_string); //pass to recursion the permission string provided by the user AND the real path of the directory given

	return EXIT_SUCCESS;
}
