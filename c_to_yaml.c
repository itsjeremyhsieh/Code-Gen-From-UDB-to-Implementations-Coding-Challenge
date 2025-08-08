#include <stdio.h>
#include <stdlib.h>
#include "sample_output/fcvt.d.q.h"
// #include "sample_output/output.h"

void print_yaml(FILE *output_file)
{
    fprintf(output_file, "$schema: \"%s\"\n", _SCHEMA);
    fprintf(output_file, "kind: \"%s\"\n", KIND);
    fprintf(output_file, "name: \"%s\"\n", NAME);
    fprintf(output_file, "long_name: \"%s\"\n", LONG_NAME);

    fprintf(output_file, "description:\n");
    fprintf(output_file, "  - id: \"%s\"\n", DESCRIPTION_0_ID);
    fprintf(output_file, "    normative: %s\n", DESCRIPTION_0_NORMATIVE ? "true" : "false");
    fprintf(output_file, "    text: |\n");

    const char *text = DESCRIPTION_0_TEXT;
    fprintf(output_file, "      ");
    for (const char *p = text; *p; ++p)
    {
        if (*p == '\\' && *(p + 1) == 'n')
        {
            fprintf(output_file, "\n      ");
            ++p;
        }
        else
        {
            fputc(*p, output_file);
        }
    }

    fprintf(output_file, "\ndefinedBy: \"%s\"\n", DEFINEDBY);
    fprintf(output_file, "assembly: \"%s\"\n", ASSEMBLY);
    fprintf(output_file, "encoding:\n");
    fprintf(output_file, "  match: \"%s\"\n", ENCODING_MATCH);
    fprintf(output_file, "  variables:\n");
    fprintf(output_file, "    - name: \"%s\"\n", ENCODING_VARIABLES_0_NAME);
    fprintf(output_file, "      location: \"%s\"\n", ENCODING_VARIABLES_0_LOCATION);
    fprintf(output_file, "    - name: \"%s\"\n", ENCODING_VARIABLES_1_NAME);
    fprintf(output_file, "      location: \"%s\"\n", ENCODING_VARIABLES_1_LOCATION);
    fprintf(output_file, "    - name: \"%s\"\n", ENCODING_VARIABLES_2_NAME);
    fprintf(output_file, "      location: \"%s\"\n", ENCODING_VARIABLES_2_LOCATION);

    fprintf(output_file, "access:\n");
    fprintf(output_file, "  s: \"%s\"\n", ACCESS_S);
    fprintf(output_file, "  u: \"%s\"\n", ACCESS_U);
    fprintf(output_file, "  vs: \"%s\"\n", ACCESS_VS);
    fprintf(output_file, "  vu: \"%s\"\n", ACCESS_VU);

    fprintf(output_file, "data_independent_timing: %s\n", DATA_INDEPENDENT_TIMING ? "true" : "false");
    fprintf(output_file, "operation(): |\n");

    fprintf(output_file, "  ");
    const char *operation = OPERATION__;
    for (const char *p = operation; *p; ++p)
    {
        if (*p == '\\' && *(p + 1) == 'n')
        {
            fprintf(output_file, "\n  ");
            ++p;
        }
        else
        {
            fputc(*p, output_file);
        }
    }
    fprintf(output_file, "\n");
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: %s <output file>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *output_filename = argv[1];
    FILE *output_file = fopen(output_filename, "w");
    if (!output_file)
    {
        perror("Failed to open output file");
        return EXIT_FAILURE;
    }

    print_yaml(output_file);
    fclose(output_file);
    return EXIT_SUCCESS;
}