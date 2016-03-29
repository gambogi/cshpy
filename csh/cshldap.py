import ldap as pyldap
from datetime import datetime, date
from copy import deepcopy
from collections import namedtuple
from member import Member

USERS = 'ou=Users,dc=csh,dc=rit,dc=edu'
GROUPS = 'ou=Groups,dc=csh,dc=rit,dc=edu'
COMMITTEES = 'ou=Committees,dc=csh,dc=rit,dc=edu'
APPS = 'ou=Apps,dc=csh,dc=rit,dc=edu'

class LDAP:

    def __init__(self, user, password,
                 host='ldaps://ldap.csh.rit.edu:636',
                 base=USERS,
                 bind=APPS,
                 app=False,
                 objects=False):
        self.host = host
        self.base = base
        self.ldap_conn = pyldap.initialize(host)
        self.ldap_conn.set_option(pyldap.OPT_X_TLS_DEMAND, True)
        self.ldap_conn.set_option(pyldap.OPT_DEBUG_LEVEL, 255)
        self.objects = objects

        if app:
            self.ldap_conn.simple_bind('cn={},{}'.format(user, APPS),
                                       password)
        else:
            try:
                auth = pyldap.sasl.gssapi("")

                self.ldap_conn.sasl_interactive_bind_s("", auth)
                self.ldap_conn.set_option(pyldap.OPT_DEBUG_LEVEL, 0)
            except pyldap.LDAPError, e:
                print 'Are you sure you\'ve run kinit?'
                print e

    def members(self, uid="*"):
        """ members() issues an ldap query for all users, and returns a dict
            for each matching entry. This can be quite slow, and takes roughly
            3s to complete. You may optionally restrict the scope by specifying
            a uid, which is roughly equivalent to a search(uid='foo')
        """
        entries = self.search(uid='*')
        if self.objects:
            return self.memberObjects(entries)
        result = []
        for entry in entries:
            result.append(entry[1])
        return result

    def member(self, user):
        """ Returns a user as a dict of attributes
        """
        try:
            member = self.search(uid=user)[0]
        except IndexError:
            return None
        if self.objects:
            return member
        return member[1]

    def eboard(self):
        """ Returns a list of eboard members formatted as a search
            inserts an extra ['commmittee'] attribute
        """
        # self.committee used as base because that's where eboard
        # info is kept
        committees = self.search(base=COMMITTEES, cn='*')
        directors = []
        for committee in committees:
            for head in committee[1]['head']:
                director = self.search(dn=head)[0]
                director[1]['committee'] = committee[1]['cn'][0]
                directors.append(director)
        if self.objects:
            return self.memberObjects(directors)
        return directors

    def group(self, group_cn):
        members = self.search(base=GROUPS, cn=group_cn)
        if len(members) == 0:
            return members
        else:
            member_dns = members[0][1]['member']
        members = []
        for member_dn in member_dns:
            members.append(self.search(dn=member_dn)[0])
        if self.objects:
            return self.memberObjects(members)
        return members

    def getGroups(self, member_dn):
        searchResult = self.search(base=GROUPS, member=member_dn)
        if len(searchResult) == 0:
            return []

        groupList = []
        for group in searchResult:
            groupList.append(group[1]['cn'][0])
        return groupList

    def drinkAdmins(self):
        """ Returns a list of drink admins uids
        """
        admins = self.group('drink')
        return admins

    def rtps(self):
        rtps = self.group('rtp')
        return rtps

    def trimResult(self, result):
        return [x[1] for x in result]

    def search(self, base=False, trim=False, **kwargs):
        """ Returns matching entries for search in ldap
            structured as [(dn, {attributes})]
            UNLESS searching by dn, in which case the first match
            is returned
        """
        scope = pyldap.SCOPE_SUBTREE
        if not base:
            base = USERS

        filterstr = ''
        for key, value in kwargs.iteritems():
            filterstr += '({0}={1})'.format(key, value)
            if key == 'dn':
                filterstr = '(objectClass=*)'
                base = value
                scope = pyldap.SCOPE_BASE
                break

        if len(kwargs) > 1:
            filterstr = '(&'+filterstr+')'

        result = self.ldap_conn.search_s(base,
                                         pyldap.SCOPE_SUBTREE,
                                         filterstr,
                                         ['*', '+'])
        if base == USERS:
            for member in result:
                groups = self.getGroups(member[0])
                member[1]['groups'] = groups
                if 'eboard' in member[1]['groups']:
                    eboard_search = self.search(base=COMMITTEES,
                                                head=member[0])
                    if eboard_search:
                        member[1]['committee'] = eboard_search[0][1]['cn'][0]
            if self.objects:
                return self.memberObjects(result)
        finalResult = self.trimResult(result) if trim else result
        return finalResult

    def modify(self, uid, base=False, **kwargs):
        if not base:
            base = USERS
        dn = 'uid={},{}'.format(uid, USERS)
        old_attrs = self.member(uid)
        new_attrs = deepcopy(old_attrs)

        for field, value in kwargs.iteritems():
            if field in old_attrs:
                new_attrs[field] = [str(value)]
        modlist = pyldap.modlist.modifyModlist(old_attrs, new_attrs)

        self.ldap_conn.modify_s(dn, modlist)

    def memberObjects(self, searchResults):
        results = []
        for result in searchResults:
            newMember = Member(result, ldap=self)
            results.append(newMember)
        return results
