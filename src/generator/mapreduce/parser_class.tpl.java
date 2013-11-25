package {{namespace}};

{{#imports}}
import {{import}};
{{/imports}}

/*
 * {{class_name}} helper.
 * @autor NPData
 */
public class {{class_name}} {

{{#items}}
    public static final int {{position_name}} = {{ position_value }};
{{/items}}

    /**
     * populate method.
     *
     * @param container
     * @param line
     * @exception IOException
     * @exception NoSuchElementException
     * @return container
     */
    public {{ class_name_container }} factory(final String line) throws IOException {
        {{ class_name_container }} obj = new {{ class_name_container }}();
        populate(obj, line);

        return obj;
    }

    /**
     * populate method.
     *
     * @param container
     * @param line
     * @exception IOException
     * @exception NoSuchElementException
     */
    public void populate( final {{ class_name_container }} container, final Text line) throws IOException {
        populate(container, line.toString());
    }

    /**
     * populate method.
     *
     * @param container
     * @param line
     * @exception IOException
     * @exception NoSuchElementException
     */
    public void populate( final {{ class_name_container }} container, final String line) throws IOException {
        final String[] chunks = line.split("\t");
        String tmp;

        try {
{{#items}}
            tmp =  {{ position_name }} >= chunks.length
                ? "" : chunks[{{ position_name }}].trim();
 
            if(tmp.isEmpty()) {
    {{#value_nullable}}
                container.{{ name_cammel }} = {{ value_default }};
    {{/value_nullable}}
    {{^value_nullable}}
                throw new NoSuchElementException("Field value of {{ name_underscore }} is not available");
    {{/value_nullable}}
            } else {
                container.{{ name_cammel }}.set({{ value_parser }});
            }
 
{{/items}}
        } catch(Exception ex) {
            throw new IOException("Wrong line: <" + line + ">", ex);
        }
    }
}
