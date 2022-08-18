pub mod smatrix_utils;
use smatrix_utils::*;

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::Path;

    #[test]
    fn it_works() {
        let chmap_file=Path::new("../../test_data/channel_map.txt");
        let ch_hm = channel_map(chmap_file).unwrap();
        for i in 1..16 {
            let v1 = ch_hm.get(&i).unwrap();
            assert_eq!(*v1, (i+3)%16+1);
        }
    }
}
