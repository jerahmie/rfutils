use std::path::Path;
use smatrix::smatrix_utils::remap_smat_at_f;

fn main() -> (){
    println!("Hello file reader");
    let path = Path::new("../../test_data/s_params_original.txt");
    remap_smat_at_f(path);
}