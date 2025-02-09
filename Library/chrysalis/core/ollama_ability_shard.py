import json
import os
import argparse
from langchain.chat_models import ChatOllama
from langchain.schema import AIMessage, HumanMessage

class Ollamalith_Ability_Shard:
    """
    Ollamalith Ability Shard - The Codex of Synthesis
    A fragment of the ancient Ollamalith, forged to construct and refine abilities.
    This shard channels raw potential into structured execution, ensuring perfection through iteration.
    """

    def __init__(self, config_path="config.json"):
        with open(config_path, "r") as f:
            config = json.load(f)
        
        self.ollama_url = config["ollama_url"]
        self.model_name = config["model_name"]
        self.max_iterations = config["max_iterations"]
        self.validation_blocks = config["validation_blocks"]
        self.output_dir = config["output_dir"]
        
        self.llm = ChatOllama(model=self.model_name, base_url=self.ollama_url)
    
    def commune_with_shard(self, prompt):
        """Links with the Ability Shard’s intelligence to extract structured knowledge."""
        response = self.llm([HumanMessage(content=prompt)])
        return response.content.strip()

    def forge_ability(self, description, language):
        """Constructs an initial ability from conceptual design."""
        prompt = f"Write a function in {language}: {description}\nEnsure best practices."
        return self.commune_with_shard(prompt)

    def analyze_integrity(self, code, language):
        """Examines the generated ability for weaknesses and inconsistencies."""
        prompt = f"Review the following {language} function:\n{code}\nIdentify issues and suggest fixes."
        return self.commune_with_shard(prompt)

    def simulate_execution(self, code, language):
        """Runs a theoretical simulation of the ability’s performance."""
        prompt = f"Simulate running this {language} function:\n{code}\nIdentify any runtime or logical issues."
        return self.commune_with_shard(prompt)

    def refine_ability(self, code, error_output, language):
        """Refines the ability, eliminating detected flaws."""
        prompt = f"Fix these issues in the {language} function:\n{error_output}\nProvide the corrected version."
        return self.commune_with_shard(prompt)

    def archive_knowledge(self, code, ability_name, language):
        """Records detailed documentation of the ability within the archives."""
        prompt = f"Generate Markdown documentation for the {language} function {ability_name}:\n{code}"
        return self.commune_with_shard(prompt)

    def final_inspection(self, code, documentation, language):
        """Conducts a final integrity scan before sealing the ability’s form."""
        prompt = f"Assess this {language} function and its documentation:\n{code}\n{documentation}"
        return self.commune_with_shard(prompt)

    def iterative_refinement(self, description, ability_name, language):
        """Cycles through iterations to perfect the ability before finalization."""
        ability_code = self.forge_ability(description, language)

        for _ in range(self.max_iterations):
            for block in self.validation_blocks:
                if block == "validate":
                    validation_feedback = self.analyze_integrity(ability_code, language)
                elif block == "simulate_compile":
                    error_output = self.simulate_execution(ability_code, language)
                    if "success" in error_output.lower():
                        break
                elif block == "refine":
                    ability_code = self.refine_ability(ability_code, error_output, language)

        documentation = self.archive_knowledge(ability_code, ability_name, language)
        assessment = self.final_inspection(ability_code, documentation, language)
        return ability_code, documentation, assessment

    def seal_into_relic(self, ability_name, code, documentation, assessment):
        """Encapsulates the ability into its final form within the archives."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        with open(f"{self.output_dir}/{ability_name}.txt", "w") as f:
            f.write(code)
        with open(f"{self.output_dir}/{ability_name}.md", "w") as f:
            f.write(documentation)
        with open(f"{self.output_dir}/{ability_name}_assessment.txt", "w") as f:
            f.write(assessment)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refine an ability with AI assistance.")
    parser.add_argument("-d", "--description", required=True, help="Ability description")
    parser.add_argument("-n", "--name", required=True, help="Ability name")
    parser.add_argument("-l", "--language", required=True, help="Programming language")
    args = parser.parse_args()

    shard = Ollamalith_Ability_Shard()
    ability_code, documentation, assessment = shard.iterative_refinement(args.description, args.name, args.language)
    shard.seal_into_relic(args.name, ability_code, documentation, assessment)
    print(f"[Completed] Files sealed in {shard.output_dir}")
