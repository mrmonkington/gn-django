.. templatefilter:: safeseq

.. function:: safeseq

    Applies the :tfilter:`safe` filter to each element of a sequence. Useful in
    conjunction with other filters that operate on sequences, such as
    :tfilter:`join`. For example::
    
        {{ some_list|safeseq|join:", " }}
    
    You couldn't use the :tfilter:`safe` filter directly in this case, as it would
    first convert the variable into a string, rather than working with the
    individual elements of the sequence.
    