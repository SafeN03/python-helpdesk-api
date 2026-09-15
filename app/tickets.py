from typing import Literal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter(prefix="/tickets", tags=["tickets"])

Priority = Literal["low", "medium", "high", "critical"]
TicketStatus = Literal["open", "in_progress", "closed"]


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Priority = "medium"


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: Priority | None = None
    status: TicketStatus | None = None


class Ticket(TicketCreate):
    id: int
    status: TicketStatus = "open"


tickets: list[Ticket] = []
next_id = 1


def find_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.id == ticket_id:
            return ticket

    raise HTTPException(status_code=404, detail="Ticket not found")


@router.post("", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(data: TicketCreate):
    global next_id

    ticket = Ticket(id=next_id, **data.model_dump())

    tickets.append(ticket)
    next_id += 1

    return ticket


@router.get("", response_model=list[Ticket])
def get_tickets():
    return tickets


@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):
    return find_ticket(ticket_id)


@router.patch("/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: int, data: TicketUpdate):
    ticket = find_ticket(ticket_id)

    changes = data.model_dump(exclude_unset=True)

    for key, value in changes.items():
        setattr(ticket, key, value)

    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int):
    ticket = find_ticket(ticket_id)
    tickets.remove(ticket)