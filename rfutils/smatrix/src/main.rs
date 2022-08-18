use std::path::Path;
use std::fs::File;
use std::io::{self, Write};
use smatrix::smatrix_utils::*;

fn main() -> io::Result<()>{
    println!("Hello file reader");
    let smat_path = Path::new(r"../../test_data/s_params_original.txt");
    let shm = get_smat_at_f(smat_path).unwrap();
    let chmap_path = Path::new(r"../../test_data/channel_map.txt");
    let chmap = channel_map(chmap_path).unwrap();
    let export_string = remap_smat_at_f(chmap, shm).unwrap();
    println!("{}", export_string);
    let mut remapped_smat = File::create(r"../../test_data/s_params_remapped.txt")?;
    remapped_smat.write_all(export_string.as_bytes())?;

    Ok(())
}