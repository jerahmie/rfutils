use std::io::Read;
use std::path::Path;
use std::fs::File;
use std::collections::HashMap;
use std::io::{self};
use regex::Regex;

pub fn get_smat_at_f(file_path: &Path) -> io::Result<HashMap<(i32,i32),String>> {
    println!("remap_smat_at_f");
    let mut f = File::open(file_path)?;
    let mut buf = String::new();
    let rg = Regex::new(r"^\( ([0-9]+) , ([0-9]+) \): (.*)").unwrap();
    let mut smat_hm: HashMap<(i32, i32), String> = HashMap::new();
    f.read_to_string(&mut buf)?;
    for line in buf.split('\n'){
        let caps = rg.captures(line);
        match caps {
            Some(caps) => {
                let i = caps.get(1)
                                 .map_or("", |m| m.as_str())
                                 .parse::<i32>().unwrap();
                let j = caps.get(2)
                                 .map_or("", |m| m.as_str())
                                 .parse::<i32>().unwrap();
                println!("{}, {}", i, j);
                smat_hm.insert((i,j), caps.get(3).map_or("".to_string(), |m| m.as_str().to_string()));
            },
            None => (),
        }
    }
    Ok(smat_hm)
}


pub fn remap_smat_at_f(coil_map: HashMap<i32, i32>, smat: HashMap<(i32,i32), String>) -> io::Result<String> {
    let mut remapped_smat = "".to_owned();
    let nchannels = coil_map.len() as i32;

    // create string from hash maps
    for i in 1..(nchannels+1) {
        for j in 1..(nchannels+1) {
            // channel number mappings:
            // ii, jj: original channel numbering
            let ii = coil_map.get(&i).unwrap(); 
            let jj = coil_map.get(&j).unwrap();

            remapped_smat.push_str("( ");
            remapped_smat.push_str(&i.to_string());
            remapped_smat.push_str(" , ");
            remapped_smat.push_str(&j.to_string());
            remapped_smat.push_str(" ):");
            remapped_smat.push_str(&smat.get(&(*ii,*jj)).unwrap());
            remapped_smat.push_str("\n");
        }
    }   
    Ok(remapped_smat)
}

pub fn channel_map(file_path: &Path) -> io::Result<HashMap<i32, i32>>{
    let mut channel_hm: HashMap<i32, i32> = HashMap::new();
    let rg = Regex::new(r"^[ ]*([0-9]+)[ ,]+([0-9]+)$").unwrap();
    let mut f = File::open(file_path)?;
    let mut buf = String::new();
    f.read_to_string(&mut buf)?;
    
    for line in buf.split('\n') {
        let caps = rg.captures(line);
        match caps {
            Some(caps) => {
                let i: i32 = caps.get(1)
                             .map_or("", |m| m.as_str())
                             .parse::<i32>().unwrap();
                let j: i32 = caps.get(2)
                             .map_or("", |m| m.as_str())
                             .parse::<i32>().unwrap();
                println!("{}, {}", i, j);
                channel_hm.insert(i, j);
                
            },
            None => (),
        }
    }
    
    Ok(channel_hm)
}