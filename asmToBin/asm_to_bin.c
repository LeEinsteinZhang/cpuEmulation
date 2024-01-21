#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *file;
    char buffer[1000];

    // 打开文件
    file = fopen("./memcpy", "r");
    if (file == NULL) {
        perror("Error in opening file");
        return(-1);
    }

    // 读取并显示文件内容
    while (fgets(buffer, 1000, file) != NULL)
        printf("%s", buffer);

    // 关闭文件
    fclose(file);

    return 0;
}