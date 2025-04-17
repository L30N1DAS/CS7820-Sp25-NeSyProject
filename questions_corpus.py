import os
import pandas as pd
from enum import Enum

# Taxonomy levels
class Taxonomy(Enum):
    Remember = 1
    Understand = 2
    Apply = 3
    Analyze = 4
    Evaluate = 5
    Create = 6

def large_questions():
    xls = pd.ExcelFile("large_Questions.xlsx")
    expert_eval_dir = "AEQG_Blooms_Evaluation_LLMs-main/generated_questions"

    # Goes through each sheet in the Excel file and each corresponding human evaluation Excel file
    for sheet_name in xls.sheet_names:
        large_df = pd.read_excel("large_Questions.xlsx", sheet_name=sheet_name)
        large_df.columns = large_df.columns.str.strip()
        large_excel_human = os.path.join(expert_eval_dir, f"{sheet_name}_ExpertEvaluation.xlsx")
        large_df_human = pd.read_excel(large_excel_human)
        large_df_human.columns = large_df_human.columns.str.strip()

        # Finds each question in the Excel file in the human evaluation Excel file
        # Determines the taxonomy level of that question
        # Writes the question and its taxonomy level on a unique line in the output file
        with open("questions_corpus.txt", "a") as f:
            for large_index, large_row in large_df.iterrows():
                for large_index_human, large_row_human in large_df_human.iterrows():
                    if large_row["Questions"] == large_row_human["Questions"]:
                        taxonomy_level = large_row_human["Index"] % 6
                        if taxonomy_level == 0:
                            taxonomy_level = 6
                        f.write(f"Taxonomy Level: {Taxonomy(taxonomy_level).name} | {str(large_row["Questions"]).replace("\n", " ")}\n")

def small_questions():
    xls = pd.ExcelFile("Questions_generated.xlsx")

    # Goes through each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        small_df = pd.read_excel("Questions_generated.xlsx", sheet_name=sheet_name)
        small_df.columns = small_df.columns.str.strip()

        # Writes each question and its taxonomy level on a unique line in the output file
        with open("questions_corpus.txt", "a") as f:
            for index, row in small_df.iterrows():
                taxonomy_level = row["Index"] % 6
                if taxonomy_level == 0:
                    taxonomy_level = 6
                f.write(f"Taxonomy Level: {Taxonomy(taxonomy_level).name} | {str(row["Questions"]).replace("\n", " ")}\n")

def main():
    small_questions()
    large_questions()

if __name__ == "__main__":
    main()
