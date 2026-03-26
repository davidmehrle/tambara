# Create all binary sequences of length n
BinarySequences := function(n)
    local subseqs, L0, L1, i;
    if n = 0 then 
        return [[]];
    else 
        subseqs := BinarySequences(n-1);
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

# Given a list L of length n and a permutation g in S_n, permute 
# the elements of the list according to the permutation g
OnIndices := function(L,g)
    return List([1..Length(L)], i -> L[i^g]);
end;

# Compute all of the stabilizers of the group action of G on X
Stabilizers := function(G,X,Action)
    local orbits; 
    orbits := Orbits(G,X,Action);
    return List(orbits, orb -> Stabilizer(G,orb[1],Action));
end; 

# Given a group G, find the permutation group representation of it
AsPermGroup := function(G)
    return Image(IsomorphismPermGroup(G)); 
end;