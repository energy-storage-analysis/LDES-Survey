# Export the vars in .env into your shell:
# https://gist.github.com/judy2k/7656bfe3b322d669ef75364a46327836
export $(egrep -v '^#' ../.env | xargs)


echo "---consolidate dataset readmes---"
cd "$REPO_DIR\cap_cost\datasets"
python consolidate_readme.py

echo "---generate SM type info table---"
cd "$REPO_DIR\cap_cost\analysis\table_gen"
python SM_type_info.py

echo "---consolidate SI docs---"
cd "$REPO_DIR\SI_docs"
python gen_SI.py