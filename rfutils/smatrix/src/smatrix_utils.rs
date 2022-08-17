use std::io::Read;
use std::path::Path;
use std::fs::File;
//use std::io::BufReader;
use std::io::{self};
use regex::Regex;

pub fn remap_smat_at_f(file_path: &Path) -> io::Result<()> {
    println!("remap_smat_at_f");
    let mut f = File::open(file_path)?;
    let mut buf = String::new();
    let rg = Regex::new(r"^\( ([0-9]+) , ([0-9]+) \): (.*)").unwrap();
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
                println!("The data: {}", caps.get(3).map_or("", |m| m.as_str()));
            },
            None => (),
        }
    }
    Ok(())
}