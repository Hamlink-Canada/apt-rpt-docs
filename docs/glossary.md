# Glossary

Terms used across Portal and the Registration and Discovery systems.

## Association

An Organisation type, often used for a regional, umbrella, or representative
body. Naming varies by country. A Repeater Association is a separate grouping
of linked repeaters.

## Central Credential System

A service that provides registration passwords to trusted registrars. It does
not handle the HTTP or IAX registration protocol.

## Discovery

Services that help nodes and network clients find currently reachable
repeaters. DNS is the current discovery interface; more services may be added
as network needs grow.

## Node ID

The numeric identity used by a repeater during registration. Portal assigns it
to a Repeater.

## Organisation

A shared amateur-radio organisation profile that can own Sites and be
referenced across products. Portal supports Club, Association, Society, League,
Union, Federation, and Other types. An Organisation's type is independent of
whether it is system-maintained.

## Portal

The generic management application for Sites, Repeaters, and Organisations. A
particular network supplies its display name and hostnames.

## Portal member

A user associated with an Organisation in Portal. The frontend supports Staff
and Viewer roles.

## PROXY protocol

A transport metadata format that carries original client and destination
endpoints through a trusted proxy. The IAX registrar supports PROXY protocol v2
over UDP/IPv4 when explicitly enabled and restricted to trusted proxy
addresses.

## Refresh Interval

How often a node resends its details to the registration system.

## Registration

A time-limited statement of the network address at which a node can be
reached.

## Registration services

Systems that authenticate nodes and publish their registration observations
for Discovery and other consumers.

## Registration Lifetime

The configured period used to determine DNS registration validity and derived
current-registration freshness.

## Registration password

A generated shared secret that proves a node's identity during registration.

## Repeater Association

A grouping of linked repeaters, potentially maintained jointly by different
Organisations. It is not an Organisation type.

## Repeater Metadata Updater

The separate planned service that consumes registration events and writes the
latest observed status to Portal.

## Runtime Portal configuration

Public deployment settings loaded by the Portal browser application at
startup, such as its display name and identity provider. It contains no
secrets.

## Site

A physical repeater location managed in Portal.

## Site ID / site code

The location identifier assigned to a Site. In short numbering mode, it is
also the Node ID of the Site's single Repeater.

## website

A public or product home page. It is distinct from a physical Site and a
management portal.

## management portal

A web application for managing network records, such as Portal. It is distinct
from a public website and a physical Site.
