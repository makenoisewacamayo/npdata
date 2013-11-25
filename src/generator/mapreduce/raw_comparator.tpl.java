package {{namespace}};

{{#imports}}
import {{import}};
{{/imports}}

/*
 * {{class_name}} container.
 * @autor NPData
 */
public class {{ class_name }} implements RawComparator<{{ class_name_container }}> {

{{ #items }}
    {{ #size_value }}
    private static final int {{ size_name }} = {{ size_value }};
    {{ /size_value }}
{{ /items }}

{{ #items }}
    private static final WritableComparator {{ comparator_name }} = new {{ comparator_obj }}();
{{ /items }}

    /**
     * compare methods.
     *
     * @param alpha the first object to be compared.
     * @param beta the second object to be compared.
     * @return a negative integer, zero, or a positive integer as the
     *         first argument is less than, equal to, or greater than the
     *         second.
     * @throws ClassCastException if the arguments' types prevent them from
     *         being compared by this comparator.
     */
    @Override
    public int compare(final {{ class_name_container }} alpha, final {{ class_name_container }} beta) {
        final byte[] alphaByte = WritableUtils.toByteArray(alpha);
        final byte[] betaByte = WritableUtils.toByteArray(beta);

        return compare(alphaByte, 0, alphaByte.length,
                betaByte, 0, betaByte.length);
    }

    /**
     * Raw comparison.
     */
    @Override
    public int compare(final byte[] alpha, int alphaStart, int alphaLength, final byte[] beta, int betaStart, int betaLength){

        int alphaFactor = alphaStart;
        int betaFactor = betaStart;
        int alphaFieldSize, betaFieldSize, delta;

        try{
{{ #items }}
            // <editor-fold defaultstate="collapsed" desc="{{ name_underscore }} comparison">
    {{ #size_value }}
            alphaFieldSize = betaFieldSize = {{ size_name }};
    {{ /size_value }}
    {{ ^size_value }}
            alphaFieldSize = WritableUtils.decodeVIntSize(alpha[alphaFactor]) + WritableComparator.readVInt(alpha, alphaFactor);
            betaFieldSize = WritableUtils.decodeVIntSize(beta[betaFactor]) + WritableComparator.readVInt(beta, betaFactor);
    {{ /size_value }}

    {{ #order_ignore }}
            // Field is ignored
    {{ /order_ignore }}
    {{ ^order_ignore }}
            {{ #order_ascending }}
            delta = {{ comparator_obj }}.compare(alpha, alphaFactor, alphaFieldSize, beta, betaFactor, betaFieldSize);
            {{ /order_ascending }}
            {{ #order_descending }}
            delta = {{ comparator_obj }}.compare(beta, betaFactor, betaFieldSize, alpha, alphaFactor, alphaFieldSize);
            {{ /order_descending }}

            if(delta != 0) {
                return delta;
            }
    {{ /order_ignore }}
    
            alphaFactor += alphaFieldSize;
            betaFactor += betaFieldSize;
            // </editor-fold>
{{ /items }}

            return 0;
        } catch(IOException ex) {
            throw new IllegalArgumentException(ex);
        }
    }
}
