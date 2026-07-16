use pyo3::prelude::*;
use std::time::{SystemTime, UNIX_EPOCH};

#[pyfunction]
fn strikes(dates: Vec<String>) -> PyResult<(i32, i32)> {
    let parsed_dates = vector_of_strike(dates);
    let mut days = Vec::new();
    
    for i in parsed_dates {
        let year = *i.get(0).unwrap_or(&0);
        let month = *i.get(1).unwrap_or(&0);
        let day = *i.get(2).unwrap_or(&0);
        
        let date_num = enum_dates([year, month, day]);
        days.push(date_num);
    }
    
    days.sort_unstable();
    days.dedup();

    let today_days = get_system_today_days();

    Ok((count_current_progress(&days, today_days), count_max_dates(&days)))
}

fn get_system_today_days() -> i32 {
    let start = SystemTime::now();
    let since_the_epoch = start
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0);

    let days_since_1970 = (since_the_epoch / 86400) as i32;
    719163 + days_since_1970
}

fn vector_of_strike(mut dates: Vec<String>) -> Vec<Vec<i32>> {
    dates.sort_unstable();
    dates.dedup();

    let mut all_data = Vec::new();
    for dates_str in dates {
        let mut parsed_data = Vec::new();
        for part in dates_str.split("-") {
            let number = match part.trim().parse::<i32>() {
                Ok(num) => num,
                Err(_) => 0,
            };
            parsed_data.push(number);
        }
        all_data.push(parsed_data);
    }
    all_data
}

fn count_max_dates(dates: &[i32]) -> i32 {
    if dates.is_empty() { return 0; }
    let mut all_days = Vec::new();
    let mut soon_days = 1;

    for days in dates.windows(2) {
        if days[0] + 1 == days[1] {
            soon_days += 1;
        } else if days[0] != days[1] {
            all_days.push(soon_days);
            soon_days = 1;
        }
    }
    all_days.push(soon_days); 
    all_days.iter().max().copied().unwrap_or(0)
}

fn count_current_progress(dates: &[i32], today_days: i32) -> i32 {
    let last_day = match dates.last() {
        Some(day) => *day,
        None => return 0,
    };

    if today_days - last_day > 1 {
        return 0;
    }

    let mut count = 1;
    for days in dates.windows(2).rev() {
        if days[0] + 1 == days[1] {
            count += 1;
        } else if days[0] == days[1] {
            continue;
        } else {
            break;
        }
    }
    count
}

fn enum_dates(date: [i32; 3]) -> i32 {
    let past_year = date[0] - 1;
    let days_from_years = past_year * 365 + (past_year / 4) - (past_year / 100) + (past_year / 400);
    let is_leap_year = is_leap(date[0]);
    let month_days = months_days_soon(is_leap_year, date[1]);

    days_from_years + month_days + date[2]
}

fn months_days_soon(is_leap_year: bool, month: i32) -> i32 {
    let number = if is_leap_year { 29 } else { 28 };
    let months = [31, number, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    months.iter().take((month - 1) as usize).sum()
}

fn is_leap(year: i32) -> bool {
    (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)
}

#[pymodule]
fn rust_analytics(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(strikes, m)?)?;
    Ok(())
}
