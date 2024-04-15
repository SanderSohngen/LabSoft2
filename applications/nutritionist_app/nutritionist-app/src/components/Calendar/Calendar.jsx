import { useEffect, useState } from 'react';
import ptLocale from '@fullcalendar/core/locales/pt'
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import { useFetchAppointments } from '../../hooks/useAppointments';
import Loading from '../Loading/Loading';

const calculateEndTime = (startTime) => {
    return new Date(new Date(startTime).getTime() + 60 * 60 * 1000).toISOString();
};

function Calendar() {
  const { data, isLoading } = useFetchAppointments("nutritionist");
  const [events, setEvents] = useState([]);

  useEffect(() => {
      if (data) {
          const formattedEvents = data.map(appointment => ({
              title: appointment.name,
              start: appointment.datetime,
              end: calculateEndTime(appointment.datetime)
          }));
          setEvents(formattedEvents);
      }
  }, [data]);

  if (isLoading) return <Loading />;

  return (
    <FullCalendar
        locale={ptLocale}
        plugins={[ timeGridPlugin ]}
        initialView="timeGridWeek"
        weekends={false}
        slotMinTime="08:00:00"
        slotMaxTime="18:00:00"
        contentHeight="auto"
        events={events}
    />
  )
}

export default Calendar;