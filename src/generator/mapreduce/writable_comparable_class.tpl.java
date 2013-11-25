package {{namespace}};

{{#imports}}
import {{ import }};
{{/imports}}

/*
 * {{ class_name }} container.
 * @autor NPData
 */
public class {{ class_name }} implements WritableComparable<{{ class_name }}> {

{{#items}}
    /**
     * {{ name_underscore }} field ({{ type_basic }}).
     * {{ #doc }}
     * {{ doc }}
     * {{ /doc }}
     */
    public final {{ type_hadoop }} {{ name_cammel }} = new {{ type_hadoop }}();;
{{/items}}

    /**
     * Returns a string representation of the object.
     * @return 
     */
    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        builder{{#items}}{{^position_first}}
               .append('\t'){{/position_first}}.append({{ name_cammel }}){{/items}};

        return builder.toString();
    }

    // <editor-fold defaultstate="collapsed" desc="WritableComparable interface">
    /**
     * Serialize the fields of this object to stream.
     *
     * @param stream DataOuput to serialize this object into.
     * @throws java.io.IOException
     */
    @Override
    public void write(final DataOutput stream) throws IOException {
{{#items}}
        {{ name_cammel }}.write(stream);
{{/items}}
    }

    /**
     * Deserialize the fields of this object from stream.
     * For efficiency, implementations should attempt to re-use storage in the existing object where possible.
     *
     * @param DataInput to deseriablize this object from.
     * @throws java.io.IOException
     */
    @Override
    public void readFields(final DataInput stream) throws IOException {
{{#items}}
        {{ name_cammel }}.readFields(stream);
{{/items}}
    }
    // </editor-fold>

    // <editor-fold defaultstate="collapsed" desc="Comparer methods">
    @Override
    public int hashCode() {
        long hash = 7;
{{#items}}
        hash += 71 * hash + {{ name_cammel }}.hashCode();
{{/items}}
        return (int) hash & Integer.MAX_VALUE;
    }

    @Override
    public boolean equals(final Object obj) {
        if (!(obj instanceof {{ class_name }})) {
            return super.equals(obj);
        }

        final {{ class_name }} other = ({{ class_name }}) obj;
        return {{#items}}{{^position_first}} 
               && {{/position_first}}{{ name_cammel }}.equals(other.{{ name_cammel }}){{/items}};
    }

    @Override
    public int compareTo(final {{class_name}} other) {
        if(other == null) {
            return 1;
        }
{{#items}}
        if(!{{ name_cammel }}.equals(other.{{ name_cammel }})) {
            {{ #order_descending }}
            return other.{{ name_cammel }}.compareTo({{ name_cammel }});
            {{ /order_descending }}
            {{ ^order_descending }}
            return {{ name_cammel }}.compareTo(other.{{ name_cammel }});
            {{ /order_descending }}
        }
{{/items}}

        return 0;
    }
    // </editor-fold>
}
