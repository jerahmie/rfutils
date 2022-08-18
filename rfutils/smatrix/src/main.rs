use std::path::Path;
use smatrix::smatrix_utils::*;

fn main() -> (){
    println!("Hello file reader");
    let smat_path = Path::new("../../test_data/s_params_original.txt");
    let shm = get_smat_at_f(smat_path).unwrap();
    let chmap_path = Path::new("../../test_data/channel_map.txt");
    let chmap = channel_map(chmap_path).unwrap();
    println!("{}", shm.get(&(1,1)).unwrap());
    println!("{}", chmap.get(&1).unwrap());
}