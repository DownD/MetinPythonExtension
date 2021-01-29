#include <iostream>
#include <fstream>
#include <sstream>

int maxX = 0;
int maxY = 0;

unsigned char* map = 0;

bool loadMapFromDisk()
{
	std::ifstream fin("metin2_map_c3.txt");

	if (fin.fail())
	{
		return false;
	}
	std::string line;
	std::getline(fin, line);
	std::stringstream sl(line);
	
	sl >> maxX >> maxY;
	if (maxX == 0 || maxY == 0) {
		return false;
	}
	map = (unsigned char*)calloc(maxX * maxY,1);
	int y = 0;
	while (std::getline(fin, line)) {
		for (int x = 0; x < maxX && x < line.size();x++) {
			if (line.at(x) == '1') {
				map[maxX * y + x] = 1;
			}
		}
		y++;
	}
	fin.close();
	return true;

}


int main(){
    loadMapFromDisk();
	for(int y = 0; y<maxY; y++){
		for(int x = 0;x<maxX;x++ ){
			printf("%d",(int)map[maxX * y + x]);
		}
	}
	printf("%d %d",maxX,maxY);
}