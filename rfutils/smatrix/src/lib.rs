use pyo3::prelude::*;
//use pyo3::wrap_pyfunction;
use numpy::{IntoPyArray, PyArray1, PyReadonlyArrayDyn};
pub mod smatrix_utils;
//use smatrix_utils::*;
use std::f64::consts::PI;


#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn deg_to_rad<'py>(py: Python<'py>, x: PyReadonlyArrayDyn<f64>) -> &'py PyArray1<f64> {
    let array = x.as_array();
    let result_array = array.into_iter()
                            .map(|xi| PI/180.0*xi)
                            .collect::<Vec<_>>();

    result_array.into_pyarray(py)
}



#[pymodule]
fn smatrix_rust(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(deg_to_rad, m)?)?; 
    Ok(())    
}

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
