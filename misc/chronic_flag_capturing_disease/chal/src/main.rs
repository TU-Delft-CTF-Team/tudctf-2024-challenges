use std::env;
use std::io;
use std::thread;
use std::time::Duration;

const SLEEP_DURATION: u64 = 1000;

fn main() {
    let flag = env::var("FLAG").unwrap_or("TUDCTF{FAKE_FLAG}".to_string());
    println!("Please enter the flag:");
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read user input.");
    println!("Checking...");
    for (ch0, ch1) in input.chars().zip(flag.chars()) {
        if ch0 != ch1 {
            break;
        }
        thread::sleep(Duration::from_millis(SLEEP_DURATION));
    }
    println!("Goodbye!");
}
