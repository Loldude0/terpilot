import React, { useState, useEffect } from 'react';
import { DayPilot, DayPilotCalendar } from "@daypilot/daypilot-lite-react";
import { setMinutes, setHours, setDay, isPast, addWeeks } from "date-fns";
import "./Calendar.css";

const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

const Calendar = ({ schedule }) => {
  const [events, setEvents] = useState([]);
  console.log(schedule);
  useEffect(() => {
    setEvents(schedule.map(event => {
      const dayOfWeek = daysOfWeek.indexOf(event.start);
      const [startHour, startMinute] = event.start_time.split(':').map(Number);
      const [endHour, endMinute] = event.end_time.split(':').map(Number);

      let startDate = setMinutes(setHours(setDay(new Date(), dayOfWeek), startHour), startMinute);
      let endDate = setMinutes(setHours(setDay(new Date(), dayOfWeek), endHour), endMinute);

      // If the start date is in the past, move it to the next week
      if (isPast(startDate)) {
        startDate = addWeeks(startDate, 1);
        endDate = addWeeks(endDate, 1);
      }

      return {
        start: new DayPilot.Date(startDate),
        end: new DayPilot.Date(endDate),
        id: DayPilot.guid(),
        text: event.text
      };
    }));
  }, [schedule]);

  const calendarConfig = {
    viewType: "Week",
    showToolTip: false,
    eventHeight: 30,
    headerHeight: 20,
    cellHeight: 20,
    durationBarVisible: false,
    timeRangeSelectedHandling: "Disabled",
    eventDeleteHandling: "Disabled"
  };

  return (
    <div className="calendar-container">
      <DayPilotCalendar
        {...calendarConfig}
        events={events}
      />
    </div>
  );
};

export default Calendar;