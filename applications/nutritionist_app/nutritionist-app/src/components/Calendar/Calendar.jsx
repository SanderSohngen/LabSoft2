import ptLocale from '@fullcalendar/core/locales/pt'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'

export default function Calendar() {
  return (
    <FullCalendar
        locale={ptLocale}
        plugins={[ dayGridPlugin, timeGridPlugin ]}
        initialView="timeGridWeek"
        weekends={false}
        slotMinTime="08:00:00"
        slotMaxTime="18:00:00"
        contentHeight="auto"
        events={[
            { title: 'evento 1', start: '2024-03-27T11:00', end: '2024-03-27T12:00'},
            { title: 'evento 2', date: '2024-03-28' }
        ]}
    />
  )
}