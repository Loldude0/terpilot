import React, { useState, useEffect } from 'react';
import { DayPilot, DayPilotCalendar } from "@daypilot/daypilot-lite-react";
import "./CalendarStyles.css";

const Calendar = ({ schedule }) => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    // Assuming schedule is an array of event objects with { start, end, text } properties
    setEvents(schedule.map(event => ({
      start: new DayPilot.Date(event.start),
      end: new DayPilot.Date(event.end),
      id: DayPilot.guid(),
      text: event.text
    })));
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