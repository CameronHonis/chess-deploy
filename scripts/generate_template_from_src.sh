#!/bin/bash

cd "$(dirname "$0")/.." || exit

template_name="template0"
if ls templates | grep -qE "template[0-9]*"; then
  # increment template number of last template
  last_file_name=$(ls templates | grep -E "template[0-9]*" | sort -r | head -n 1)
  last_file_num_w_yml=${last_file_name#"template"}
  last_file_num=${last_file_num_w_yml%".yml"}
  template_name="template$((last_file_num + 1)).yml"
fi

template_contents=""
while read -r src_file_name; do
  template_contents+="---\n$(cat "$src_file_name")\n"
done < <(find templates/src -type f)

echo -e "$template_contents" > "templates/$template_name"
echo "Generated templates/$template_name"