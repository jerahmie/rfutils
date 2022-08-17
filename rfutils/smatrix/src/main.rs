use std::path::Path;
use smatrix::smatrix_utils::*;

fn main() -> (){
    println!("Hello file reader");
    let path = Path::new("../../test_data/s_params_original.txt");
    let shm = get_smat_at_f(path).unwrap();
    println!("{}", shm.get(&(1,1)).unwrap());
}