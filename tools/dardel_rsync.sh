rsync -av \
    --exclude='input*.hdf5' \
    --exclude='log/' \
    dardel-ftn01.pdc.kth.se:$1 $2
