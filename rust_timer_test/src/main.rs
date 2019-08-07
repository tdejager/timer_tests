use std::{thread, time};
use tokio::prelude::*;
//use tokio::timer::Interval;
use tokio_os_timer::Interval;
use std::sync::{Mutex, Arc};
use std::time::Instant;

const ITERS: u32 = 100;

fn print_stats(times: &Vec<u128>) {
    let mut min: u128 = std::u128::MAX;
    let mut max: u128 = 0;
    let mut avg: f64 = 0.0;


    for t in times.iter() {
        max = std::cmp::max(max,*t);
        min = std::cmp::min(min, *t);
        avg += *t as f64 / times.len() as f64;
    }

    println!("Avg: {}, Max: {}, Min: {}", avg, max, min);
}

fn regular_sleep() -> Vec<u128> {
    let mut times = Vec::new();

    // Measure time
    for _ in 0..ITERS {
        let now = time::Instant::now();
        thread::sleep(time::Duration::from_millis(4));
        let elapsed = now.elapsed();
        times.push(elapsed.as_micros());
    }
    times

}

fn tokio_sleep() -> Vec<u128> {
    let times = Arc::new(Mutex::new(Vec::new()));
    let instant = Arc::new(Mutex::new(Instant::now()));
    let t = times.clone();
    let instant_clone = instant.clone();

    // Tokio timer sleep
    let task = Interval::new(time::Duration::from_millis(4))
        .unwrap()
        .take(ITERS as u64)
        .for_each(move |instant| {
            let now = time::Instant::now();
            t.lock().unwrap().push(now.duration_since(instant_clone.lock().unwrap().clone()).as_micros());
            *instant_clone.lock().unwrap() = now;
//            t.lock().unwrap().push(instant.duration_since(instant_clone.lock().unwrap().clone()).as_micros());
//            *instant_clone.lock().unwrap() = instant;
            Ok(())
        })
        .map_err(|e| panic!("interval errored; err={:?}", e));

    tokio::run(task);
    let vec = times.lock().unwrap();
    vec.clone()
}


fn main() {
    print_stats(&regular_sleep());
    print_stats(&tokio_sleep());
}
