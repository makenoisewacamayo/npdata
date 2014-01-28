SET job.name '{{ entity_name }}_diff';

actual = LOAD '$actual' USING PigStorage('\t') AS (
{{#items}}
    {{ name_underscore }} : {{ type_pig }}{{ separator_comma }}
{{/items}}
);

expected = LOAD '$expected' USING PigStorage('\t') AS (
{{#items}}
    {{ name_underscore }} : {{ type_pig }}{{ separator_comma }}
{{/items}}
);

qa_cross = JOIN expected BY ({{#qakey}}{{ name_underscore }}{{ separator_comma }}{{/qakey}}) FULL,
                  actual BY ({{#qakey}}{{ name_underscore }}{{ separator_comma }}{{/qakey}});

SPLIT qa_cross INTO qa_only_expected IF {{#qakey}}actual::{{ name_underscore }} IS NULL 
                                        AND NOT expected::{{ name_underscore }} IS NULL{{ separator_and_comma }}
                                        {{/qakey}} 
                    qa_only_actual   IF {{#qakey}}NOT actual::{{ name_underscore }} IS NULL
                                        AND expected::{{ name_underscore }} IS NULL{{ separator_and_comma }}
                                        {{/qakey}} 
                    qa_both_side     IF {{#qakey}}NOT actual::{{ name_underscore }} IS NULL
                                        AND NOT expected::{{ name_underscore }} IS NULL{{ separator_and_semicolon }}
                                        {{/qakey}} 

qa_only_expected_normalized = FOREACH qa_only_expected GENERATE
{{#items}}
    expected::{{ name_underscore }} AS {{ name_underscore }}{{separator_comma_semicolon}}
{{/items}}

qa_only_actual_normalized = FOREACH qa_only_actual GENERATE
{{#items}}
    actual::{{ name_underscore }} AS {{ name_underscore }}{{ separator_comma_semicolon }}
{{/items}}

qa_both_side_normalized = FOREACH qa_both_side GENERATE
{{#qakey}}
    expected::{{ name_underscore }} AS {{ name_underscore }},
{{/qakey}}
{{#qavalue}}
    expected::{{ name_underscore }} AS expected_{{ name_underscore }},
    actual::{{ name_underscore }} AS actual_{{ name_underscore }},
    ((expected::{{ name_underscore }} == actual::{{ name_underscore }}) ? 1 : 0) AS assert_{{ name_underscore }}{{ separator_comma_semicolon }}
{{/qavalue}}

STORE qa_only_expected_normalized INTO '$output_path/{{ entity_name }}_only_expected' USING PigStorage ('\t');
STORE qa_only_actual_normalized INTO '$output_path/{{ entity_name }}_only_actual' USING PigStorage ('\t');
STORE qa_both_side_normalized INTO '$output_path/{{ entity_name }}_in_both_side' USING PigStorage ('\t');
