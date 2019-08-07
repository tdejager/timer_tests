#include <asio/io_service.hpp>
#include <asio/steady_timer.hpp>
#include <cstdint>
#include <functional>
#include <thread>
#include <iostream>

// Number of iterations, change this if you want to change how often to iterate
constexpr uint16_t ITERS = 100;

// Time
uint16_t timer_timeouts = 0;

// Statistics vector
std::vector<long> time_taken;

// Time point to set
std::chrono::time_point<std::chrono::steady_clock> t1;

/**
 * Called when the asio timer expires
 * @param timer the timer to set this callback on again
 * @param ec the error code, is set when an interrupt occurs for example
 */
void timer_callback(asio::steady_timer &timer, const std::error_code &ec) {
  timer_timeouts++;
  auto duration = std::chrono::steady_clock::now() - t1;
  time_taken.push_back(std::chrono::duration_cast<std::chrono::microseconds>(duration).count());

  // Iterate until we have done it for ITER timer_timeouts, and collect stats
  if (timer_timeouts < ITERS) {
    // Set the timer again, else it will not go off
    timer.expires_from_now(std::chrono::microseconds(4000));
    timer.async_wait(
        [&timer](std::error_code code) { timer_callback(timer, code); });
    t1 = std::chrono::steady_clock::now();
  }
}

/**
 * Given a vector of duration calulcate and print the average, max and minimum time
 * taken
 * @param time_taken the vector containing the time points
 */
void print_sleep(const std::vector<long>& time_taken) {
  double avg = 0.0;
  long max = 0;
  long min = std::numeric_limits<long>::max();

  for (auto &t : time_taken) {
    avg += (double) t / time_taken.size();
    max = std::max(max, t);
    min = std::min(min, t);
  }

  std::cout << "(micros) Avg: " << avg << ", max: " << max << ", min: " << min
            << std::endl;
}

void regular_sleep() {

  for(uint16_t i = 0; i < ITERS; i++) {

    // Set the first time point
    t1 = std::chrono::steady_clock::now();
    // Sleep..
    std::this_thread::sleep_for(std::chrono::microseconds(4000));
    // Get the taken duration
    auto duration = std::chrono::steady_clock::now() - t1;
    time_taken.push_back(
        std::chrono::duration_cast<std::chrono::microseconds>(duration)
            .count());

  }

  // Print the statistics
  print_sleep(time_taken);
}

void asio_sleep() {
  // Create an asio service to dispatch async tasks
  asio::io_service service;

  // Create a timer which expires
  asio::steady_timer timer(service);
  timer.expires_from_now(std::chrono::microseconds(4000));

  // Set the callback function and return the time
  timer.async_wait(
      [&timer](std::error_code code) { timer_callback(timer, code); });
  t1 = std::chrono::steady_clock::now();

  // Run the timer functions
  service.run();

  // Print the time taken to sleep
  print_sleep(time_taken);
}

int main() {

  // Run the regular sleeps
  std::cout << "Regular ";
  regular_sleep();

  time_taken.clear();

  // Run the asio functions
  std::cout << "Asio ";
  asio_sleep();




  return 0;
}