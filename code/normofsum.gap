binarySequences := function(n)
    local subseqs, L0, L1, i;
    if n = 0 then 
        return [[]];
    else 
        subseqs := binarySequences(n-1);
        L0 := StructuralCopy(subseqs); 
        L1 := StructuralCopy(subseqs); 
        for i in [1..Length(subseqs)] do
            Add(L0[i],0);
            Add(L1[i],1);
        od;
        Append(L0,L1);
        return L0;
    fi; 
end;

action := function(seq,sigma)
    return List([1..Length(seq)], i -> seq[i^sigma]);
end;